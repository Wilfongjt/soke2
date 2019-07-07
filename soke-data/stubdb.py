import boto3
import json
import time
from os import path
from util import Util

class StubDB:
    def __init__(self,\
                 db_name='dynamodb',\
                 region_name='us-east-2',\
                 endpoint_url='http://localhost:8000/',\
                 aws_access_key_id='anything',\
                 aws_secret_access_key='anything'):

        # print('db_name: ', db_name)
        # print('region_name: ', region_name)
        # print('endpoint_url: ', endpoint_url)
        # print('aws_access_key_id: ', aws_access_key_id)
        # print('aws_secret_access_key: ', aws_secret_access_key)
        self.dryrun = True
        self.dbName = db_name
        self.endpoint_url = endpoint_url
        self.aws_access_key_id=aws_access_key_id # suitable for local dynamodb
        self.aws_secret_access_key=aws_secret_access_key # suitable for local dynamodb
        self.region_name=region_name #'us-east-2'

        # aws dynamodb list-tables --endpoint http://localhost:8000
        # print('todo: add .env aws_access_key_id')
        # print('todo: add .env aws_secret_access_key')

        self.db = None
        self.client = None

        self.table_name_list = None
        # self.table_definitions = {}
        self.table_histories = {}
        print('------------')
        
    def connect(self, local_remote):
        if local_remote == 'local':
            print('connecting to local dynamodb')
            self.connect_local()
        else:
            self.connect_remote()
        return self 

    def connect_remote(self):

        print('remote db connecting...')
        self.db = boto3.resource(self.dbName,
                                 aws_access_key_id=self.aws_access_key_id,
                                 aws_secret_access_key=self.aws_secret_access_key,
                                 region_name=self.region_name
                                )
        
        print('remote client connecting...')
        self.client = boto3.client(self.dbName,

                                   aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key,
                                   region_name=self.region_name
                                  )
        
        print('connecting...out')
        return self

    def connect_local(self):

        print('local db connecting...')
        self.db = boto3.resource(self.dbName,
                                 endpoint_url=self.endpoint_url,
                                 aws_access_key_id=self.aws_access_key_id,
                                 aws_secret_access_key=self.aws_secret_access_key,
                                 region_name=self.region_name
                                )
        print('self.db: ', self.db)
        print('local client connecting...')
        self.client = boto3.client(self.dbName,
                                   endpoint_url=self.endpoint_url,
                                   aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key,
                                   region_name=self.region_name
                                  )
        print('list tables: ',self.client.list_tables())

        print('connecting...out')
        return self

    def getTableName(self,table_name_key):
        return self.table_histories[table_name_key][0]['TableName']

    def setAwsAccessKeyId(self, aws_access_key_id):
        self.aws_access_key_id = aws_access_key_id
        return self

    def setAwsSecretAccessKey(self, aws_secret_access_key):
        self.aws_secret_access_key = aws_secret_access_key
        return self

    def setRegionName(self, region_name):
        self.region_name
        return self

    def loadTableHistories(self, table_histories_file_name='table.histories.json', env_suffix='dev'):
        self.table_histories = {}
        with open(table_histories_file_name) as json_file:
            self.table_histories = json.load(json_file)

        for tb in self.table_histories:
            print('tb: ', tb)


        print('---------')
        return self

    '''
    def load_batch_table_data(self, table_list):
        #utils = Util()
        #tbl_list = utils.getFileList('./data/','.txt')
        print('load_batch_table_data')
        for tablename in table_list:
            print('table: ' , tablename)
    '''
    def getInputJSON(self, json_file, env_suffix):
        inputJson = json.load( json_file )
        if env_suffix != 'prod': # rekey dictionary
            tmp = {}
            for k in inputJson:
                nkey = '{}_{}'.format(k,env_suffix)
                tmp[nkey] = inputJson[k]
            inputJson = tmp
        return inputJson

    def loadBatchTableData(self, table_name_key, env_suffix, output_type):
        # output types: 'local'
        # tablename is not the same as the source file
        # the json to be loaded is keyed without the env_suffix.
        # convert the key to reflect the env_suffix before calling batch load
        util=Util()
        if output_type == 'local':
            tablename = self.table_histories[table_name_key][0]['TableName']
            tablename = table_name_key
            #for tablename in self.table_histories:
            #print('tablename: ', tablename)
            i = 0
            ticker = 0 
            #source_file = './{}/output/{}.{}.json'.format(table_name_key, i, tablename)
            source_file = '{}/{}.{}.json'.format(util.getOutputFolder(table_name_key), i, tablename )
            
            print('source_file: ', source_file)
            print('wait...')
            while path.exists(source_file):
                
                #if ticker == 50:
                #    print('source: ', source_file)
                #    ticker = 0
    
                with open(source_file) as json_file:
                    # fix the dictionary key to reflec env
                    data = self.getInputJSON( json_file, env_suffix )

                # load the data
                if self.dryrun:
                    print('Dryrun is ON: ',source_file)
                else:    
                    self.client.batch_write_item(RequestItems=data)
                
                i += 1
                # next file to load
                #source_file = './{}/output/{}.{}.json'.format(table_name_key, i, tablename)
                ticker += 1
                source_file = '{}/{}.{}.json'.format(util.getOutputFolder(table_name_key), i, tablename )


                #if i % 10:
                #    print('source: ', source_file)
                    
            print('Done')
    '''
    def loadBatchTableData(self, table_name_key, output_type):
        # output types: 'local'
        # tablename is not the same as the source file
        if output_type == 'local':
            tablename = self.table_histories[table_name_key][0]['TableName']

            #for tablename in self.table_histories:
            print('tablename: ', tablename)
            i = 0

            source_file = './{}/output/{}.{}.json'.format(table_name_key, i, tablename)

            while path.exists(source_file):
                source_file = './{}/output/{}.{}.json'.format(table_name_key, i, tablename)
                print('source: ', source_file)

                with open(source_file) as json_file:
                    data = json.load( json_file ) # get contents of json file
                    #print('data: ', data)
                    print('tablename: ', tablename)
                    table = self.getTable( tablename ) # get dynamodb table object
                    with table.batch_writer() as batch:
                        #print('write batch')
                        akey = '{}.json'.format(tablename.lower())
                        r = 0
                        for j in data[akey]:
                            print(' ')
                            print('write : ',r, j['PutRequest']['Item'])
                            batch.put_item(Item=j['PutRequest']['Item'])
                            r+=1
                        #print('\nload complete!')

                i+=1

            #else:
            #    print('path {} not exists '.format( source_file))
            print('Done')
    '''

    def dep_loadAllTableData(self):

        for tablename in self.table_definitions:
            print('tablename: ', tablename)

            if path.exists('./data/output/{}.json'.format(tablename)):
                with open('./data/output/{}.json'.format(tablename)) as json_file:
                    data = json.load(json_file)
                    # print('data: ', data)
                    table = self.getTable( tablename )
                    #print('keys', data.keys())
                    for j in data[tablename]:
                        print('j: ', j)
                        print('PutRequest: ', j['PutRequest'])
                        print('Item: ', j['PutRequest']['Item'])
                        sz = len(json.dumps(j['PutRequest']['Item']))
                        if sz > 1000:
                            print('size: ', str( len(sz) ) )
                            print('item: ',j['PutRequest']['Item'])
                        table.put_item(Item=j['PutRequest']['Item'])

                    print('\nload complete!')

            else:
                print('tablename {} not exists '.format( tablename))

        #with open(table_def) as json_file:

    def dep_createAllTables(self):
        '''
        load from list of files on disk
        '''

        for tbl_name in self.table_definitions:
            print('--')
            print('tbl_name: ', tbl_name)

            #if not self.isTable(tbl_name):
            print('creating: {}'.format(tbl_name))
            tdef = self.table_definitions[tbl_name]

            print('tdef: ', tdef)
            table = self.client.create_table(**tdef)
            waiter = self.client.get_waiter('table_exists')
            waiter.wait(TableName=tbl_name)
            #time.sleep(10)
            #table.meta.client.get_waiter('table_exists').wait(TableName=tbl_name)

        #print('waiting...',time.sleep(10))
        #time.sleep(20) #wait 20 seconds

    def dep_createTable(self, tbl_name):
        #if not self.isTable(tbl_name):
        try:
            print('createTable')
            print('find {}'.format(tbl_name))
            tdef = self.table_definitions[tbl_name]

            table = self.client.create_table(**tdef)

            print('creating ', tbl_name)
            time.sleep(20) #wait 20 seconds

            self.refreshTableList()
        except:
            print('create failed for {}'.format(tablename))

    def deleteTable(self, tablename):
        rc = False
        #if tablename in self.getTableList():
        try:
            print('deleting {}'.format(tablename))
            table = self.db.Table(tablename)
            table.delete()
            print('deleteing 2')
            #waiter = this.client.get_waiter('table_not_exists')
            #waiter.wait(TableName=tablename)
            print("table deleted")
            #time.sleep(10) #wait 20 seconds
            #self.refreshTableList()
            # print('deleted {}'.format(tablename))
            rc = True
        except:
            print('!!!!!!!!!!! delete failed for {}'.format(tablename))

        return rc

    def getClient(self):
        return self.client

    def getDb(self):
        return self.db

    def refreshTableList(self):
        self.table_name_list = []
        responce = self.client.list_tables()
        # responce = self.client.list_tables(ExclusiveStartTableName='string', Limit=100)

        self.table_name_list = responce['TableNames']
        return self

    def getTableList(self):
        '''
        returns list of table names
        force = True reloads list
        '''
        #if self.table_name_list == None:
        #    self.table_name_list = []
        #    responce = self.client.list_tables()
        #    # responce = self.client.list_tables(ExclusiveStartTableName='string', Limit=100)
        #    self.table_name_list = responce['TableNames']

        self.table_name_list = []
        responce = self.client.list_tables()
        # responce = self.client.list_tables(ExclusiveStartTableName='string', Limit=100)
        self.table_name_list = responce['TableNames']

        return self.table_name_list

    def dep_isTable(self, tblName):

        if tblName in self.getTableList():
            return True

        return False

    def getTable(self, tbl_name):
        table = None
        # tbl_name = 'users'
        #if self.isTable(tbl_name):
        #    table = self.db.Table(tbl_name)

        table = self.db.Table(tbl_name)

        return table

    def getMeta(self):
        return {
            'table_histories': self.table_histories
        }
    
    def getTableDescription(self, table_name):
        
        return self.db.DescribeTable({"TableName": table_name}) 
