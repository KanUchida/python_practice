# -*- coding:urf-8 -*-

#tagの名前が一致するものを探して、そのtagの名前と実行時間をimageを作成する
#イメージをデリートする

import json

import boto3
from boto3.session import Session

import time
from datetime import datetime as dt

import pprint #組み込み関数

#これらの存在意義は？
#おそらく必要ない
#TAGお中身
TAG_KEY_BACKUP_GENERATION = 'Backup-Generation' #世代数
TAG_KEY_AUTO_BACKUP       = 'Backup-Type' #
TAG_VAL_AUTO_BACKUP       = 'auto'


print('Loading function')

pp = pprint.PrettyPrinter(indent=4) #調べても不明

# 関数名 ： lambda_handler
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    #ec2の情報を拾ったり、タスク管理？resourceとの区別はわからない
    ec2_client   = boto3.client('ec2')

    #resourceでアクション系の操作、停止中のマシンを起動したり、停止させたり
    ec2_resource = boto3.resource('ec2')

    ret = execute_ami_backup_task(ec2_client, ec2_resource)
    print 'AMI buckup task is completed(%s).' % (ret)

    return 0
    raise Exception('Something went wrong')


# 関数名 ： execute_ami_backup_task
# 戻り値 ： 実行結果
# 引数　 ： ec2_client
#       ： ec2_resource
# 機能　 ： AMIバックアップを実行する
#          INSTANCE_ID_BACKUP　リストの中にあるやつを順にバックアップ取っていく
#          となると、 is_target でバックアップの要否を確認する必要もない
def execute_ami_backup_task(ec2_client, ec2_resource):
	#引数を指定していないから、ec2のインスタンス情報を全てとってきて、responseにいれる
	#ここの情報は、awsの画面入って、インスタンスをクリックした時に、下のほうに表示されるやつ
    response = ec2_client.describe_instances()

    #バックアップした時の時間を取っておく
    exec_time = dt.now().strftime('%Y%m%d%H%M%S')

    result = True
    #responseの唯一のkeyであるReservationsのvalueをec2_groupにいれる
    #ここは一部変更が必要
    #INSTANCE_ID_BACKUP を利用して、バックアップを取りたいインスタンスの情報をとってくる
    #この関数を探さなくちゃダメ
    for ec2_group in response['Reservations']:
    	#ec2_group(dict）のkeyのうちの１つであるInstancesの値をinstance_infoにいれる
        for instance_info in ec2_group['Instances']:
        	#バックアップしなくちゃいけないかを確認する
        	#インスタンスのIDをハードコードするから、恐らくこれは必要ない
            ret = is_target(instance_info)

            #もしもバックアップ必要なかったら、何もしないでcotinue
		    #continueはつまり、ループ処理を終えて、次のforの中身を実行する
		    #ちなみに、breakだったらfor文自体をストップさせる
		    #is_target がいなくなるからこの２行もいらなそう
            if (ret == False):
                continue

            #backup imageを作成する関数を実行する
            #画面から見るならば、「インスタンスの画面->インスタンスクリック->アクション->イメージの作成」
            #を担当する関数を呼び出して、実行結果をretに入れている部分がここ
            #これは必要
            ret = create_buckup_image(ec2_client, ec2_resource, instance_info, exec_time)
            if not ret:
                print 'create_buckup_image(%s) was failed.' % (instance_info['InstanceId'])
                result = False

                continue
            #delete だからこれも必要
            ret = delete_old_image(ec2_client, ec2_resource, instance_info)
            if not ret:
                print 'delete_old_image(%s) was failed.' % (instance_info['InstanceId'])
                result = False

                continue
    return result


# 関数名 ： is_target
# 戻り値 ： バックアップ要否
# 引数　 ： instance_info <dict>
# 機能　 ： バックアップ要否を判定する
#     必要ないかもしれん( バックアップするインスタンスをIDで直接指定するから )
def is_target(instance_info):
    val = get_tag_value(
        instance_info, 
        TAG_KEY_BACKUP_GENERATION
    )

    if val is None:
        return False

    return True


# 関数名 ： get_tag_value
# 戻り値 ： タグ値（当該キーに合致するものがなければNone）
# 引数　 ： instance_info <dict>
#       ： key <str>
# 機能　 ： インスタンス情報から指定キーのタグ値を取得する
def get_tag_value(instance_info, key):
    tags = instance_info['Tags']
    for tag in tags:
    	#tagのKeyの値がkey(引数で渡した時に自分で設定した値)じゃなかったらスキップ
    	#ここのif文の後にいけるやつは、tagにbackupが存在する
    	#設定漏れとかあった場合のerrorを除くための処理
        if not (key == tag['Key']):
            continue

        #backupの名前のtagの値が見つかったら、その値を返す
        return tag['Value']
    #for の中で何も返ってこなかった場合にはNoneを返すようにする
    return None


# 関数名 ： create_buckup_image
# 戻り値 ： 実行結果
# 引数　 ： ec2_client
#       ： ec2_resource
#       ： instance_info <dict>
#       ： exec_time <str>
# 機能　 ： バックアップイメージを作成する
def create_buckup_image(ec2_client, ec2_resource, instance_info, exec_time):
    inst_id = instance_info['InstanceId']
    #tagの中で、ここで与えた'Name'に一致するkeyを持つものがあれば、その値が返ってくる
    #引数で与えた'Name'と一致するkeyがなければNoneが返ってくるのでそれを取り除く
    #IMのインスタンスには タグ に全て Name が入っているから、これを使って良い
    name = get_tag_value(instance_info, 'Name')
    if name is None:
        print('Get name error!!')

        return False

    #インスタンスに名前をつける　名前はこれでよし

    image_name = name + '-' + exec_time

    #”NameタグのValue＋時間”を名前にして、イメージを作成する
    response = ec2_client.create_image(
        InstanceId  = inst_id,
        Name        = image_name,
        Description = image_name,
        NoReboot    = True
    )

    image_id = response['ImageId']
    print '%s was created.' % (image_id)

    #念のため、タグ設定対象のイメージ＆スナップショットが出来上がるまで待つ
    #ここから下は恐らく必要がない　タグやスナップショットに名前をつけるならば必要になる
    #タグ・スナップショットに名前をつけいたいかは松田さんに確認する(多分無いと思う)
    time.sleep(10)

    tags  = construct_backup_tags(instance_info)
    image = ec2_resource.Image(image_id)

    set_tags_to_image(image, tags)

    set_tags_to_snapshot(ec2_resource, image, tags, image_name)

    return True



# 関数名 ： delete_old_image
# 戻り値 ： 実行結果
# 引数　 ： ec2_client
#       ： ec2_resource
#       ： instance_info <dict>
# 機能　 ： 保持世代よりも古いイメージを削除する
def delete_old_image(ec2_client, ec2_resource, instance_info):
    sorted_images = get_sorted_images(ec2_client, instance_info)

    #TAG_KEY_BACKUP_GENERATION に一致した関数のtagのValueが返ってくる
    #tagのつけ方をどうしているのかがわからない
    generation = int(get_tag_value(instance_info, TAG_KEY_BACKUP_GENERATION))
    cnt = 0
    for img in sorted_images:
        cnt += 1
        if generation >= cnt:
            continue

        image_id  = img['ImageId']
        snapshots = get_snapshots(ec2_resource, image_id)

        # AMIイメージを解放する
        ec2_client.deregister_image(
            ImageId = image_id
        )
        print '%s was deregistered.' % (image_id)

        # 解放完了まで待つ
        time.sleep(10)

        # 対応するスナップショットを削除する
        for snapshot in snapshots:
            snapshot.delete()
            print '%s was deleted.' % (snapshot)

    return True


# 関数名 ： get_sorted_images
# 戻り値 ： ソート済みイメージ <list>
# 引数　 ： ec2_client
#       ： instance_info <dict>
# 機能　 ： 作成された日付順でソートしたAMIイメージリストを取得する
def get_sorted_images(ec2_client, instance_info):
    sorted_images = []
    name     = get_tag_value(instance_info, 'Name')

    #いじったり獲得したりできるimageを引っ張ってくる
    #いろいろな条件で拾ってきてあげられる
    #戻り値は、imageごとにそれぞれの特徴が入ってかえってくる。boto3のdocument参照
    response = ec2_client.describe_images(
	    #owner の種類によってimageをフィルターする
	    #selfの場合、requestを送った人が実行することになる
        Owners  = ['self'],
        Filters = [{'Name': 'tag:Name',                   'Values': [name]},
                   {'Name': 'tag:' + TAG_KEY_AUTO_BACKUP, 'Values': [TAG_VAL_AUTO_BACKUP]}]
    )

    #list型になっているイメージの一覧を取得{Images : [ここに一覧入っている]}
    images = response['Images']

    #作られた日でそれを並び替え
    sorted_images = sorted(
        images, 
        #lambda関数は無名関数と呼ばれる。 xを与えて、コロンの後にその条件を書くと、それに従った値が戻ってくる
        key = lambda x: x['CreationDate'], 
        reverse = True
    )

    return sorted_images


# 関数名 ： get_snapshots
# 戻り値 ： スナップショット群 <list>
# 引数　 ： ec2_resource
#       ： image_id <str>
# 機能　 ： AMIイメージに包含されるスナップショット群を取得する
def get_snapshots(ec2_resource, image_id):
    snapshots = []
    image     = ec2_resource.Image(image_id)

    for dev in image.block_device_mappings:
        if not dev.has_key('Ebs'):
            continue

        snapshot_id = dev['Ebs']['SnapshotId']
        snapshot    = ec2_resource.Snapshot(snapshot_id)

        snapshots.append(snapshot)

    return snapshots



# ------------------------ 以下、おそらく不要 ----------------------------


# 関数名 ： construct_backup_tags
# 戻り値 ： タグ群
# 引数　 ： instance_info <dict>
# 機能　 ： バックアプ設定用のタグ群を構成する
def construct_backup_tags(instance_info):
    ret_tags = []
    tags = instance_info['Tags']
    for tag in tags:
        if (TAG_KEY_BACKUP_GENERATION == tag['Key']):
            continue

        ret_tags.append(tag)

    t = {u'Value': TAG_VAL_AUTO_BACKUP, u'Key': TAG_KEY_AUTO_BACKUP}
    ret_tags.append(t)

    return ret_tags


# 関数名 ： set_tags_to_image
# 戻り値 ： non
# 引数　 ： image
#       ： tags <list>
# 機能　 ： AMIイメージにタグ情報を設定する
def set_tags_to_image(image, tags):
    image.create_tags(Tags = tags)

    return


# 関数名 ： set_tags_to_snapshot
# 戻り値 ： non
# 引数　 ： ec2_resource
#       ： image
#       ： tags <list>
#       ： image_name <str>
# 機能　 ： スナップショットにタグ情報を設定する
def set_tags_to_snapshot(ec2_resource, image, tags, image_name):
    for dev in image.block_device_mappings:
        # EBS以外は対象外
        if not dev.has_key('Ebs'):
            continue

        # Nameタグ差し替えのため、一旦削除
        name_idx = get_name_tag_index(tags)
        tags.pop(name_idx)

        # Nameタグ設定
        dev_name = dev['DeviceName'][5:]
        name = image_name + '-' + dev_name
        t = {u'Value': name, u'Key': 'Name'}
        tags.append(t)

        snapshot_id = dev['Ebs']['SnapshotId']
        snapshot = ec2_resource.Snapshot(snapshot_id)

        snapshot.create_tags(Tags = tags)

    return


# 関数名 ： get_name_tag_index
# 戻り値 ： Nameタグのインデックス位置（当該キーに合致するものがなければNone）
# 引数　 ： tags <list>
# 機能　 ： タグリストの中でNameタグのインデックス位置を取得する
def get_name_tag_index(tags):
    idx = 0
    for tag in tags:
        if tag['Key'] == 'Name':
            return idx

        idx += 1

    return None
