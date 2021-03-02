import json
import os






class connect:    
    def __init__(self, filename):
        self.filename = filename

        check_file_exits=os.path.isfile(filename+'.json')
        if check_file_exits==False:
            fob=open(filename+'.json','w+')
            fob.close()
            print('New File Created')
            pass
        else:
            print('File Already exixts, Connection Created...')
            pass


    def create(self,data):
        file_size=os.stat(self.filename+'.json').st_size
        #print(file_size)
        if file_size!=0:
                print('Table Already Created')
                #return False
                
        json_object = json.dumps(data, indent = 4) 
        with open(self.filename+".json", "w") as outfile:
                outfile.write(json_object)
                outfile.close()
        print('New Table Created')
        #return True


    def insert(self,data):
        with open(self.filename+'.json', 'r') as openfile:
                json_object = json.load(openfile)

        existing_data_keys=[]
        for key,value in json_object[0].items():
                existing_data_keys.append(key)

        for i in data:
            if i not in existing_data_keys:
                print('Cannot Insert !!!, Keys Mismatch')
                #return False


        remaining_list = list(set(existing_data_keys) - set(list(data)))

        for i in remaining_list:
            data[i]=None
   

        json_object.append(data)                
        json_object = json.dumps(json_object, indent = 4)

        with open(self.filename+".json", "w") as outfile:
                outfile.write(json_object)
                outfile.close()
        print('One Entry Inserted')
        #return True


    def alter_rename_column(self,old_key,new_key):
        #print(old_key,new_key)
        with open(self.filename+'.json', 'r') as openfile:
                json_object = json.load(openfile)
        #check if old key present or not
        existing_data_keys=[]
        for key,value in json_object[0].items():
                existing_data_keys.append(key)
        if old_key not in existing_data_keys:
                print('Cannot Insert!!!, Key Not Present')
                #return False


        #updating old key to new key        
        for i in json_object:
            i[new_key]=i[old_key]
            del i[old_key]

        json_object = json.dumps(json_object, indent = 4)

        with open(self.filename+".json", "w") as outfile:
                outfile.write(json_object)
                outfile.close()
        print('Key Altered')
        #return True

    def alter_add_column(self,column_name):
        with open(self.filename+'.json', 'r') as openfile:
                json_object = json.load(openfile)
        #check if old key present or not
        existing_data_keys=[]
        for key,value in json_object[0].items():
                existing_data_keys.append(key)
        if column_name in existing_data_keys:
                print('Cannot Insert Column!!!, Already Exixts')
                #return False

        for i in json_object:
            i[column_name]=None

        json_object = json.dumps(json_object, indent = 4)

        with open(self.filename+".json", "w") as outfile:
                outfile.write(json_object)
                outfile.close()
        print('Column Added')
        #return True


    def delete(self,data):
        with open(self.filename+'.json', 'r') as openfile:
                json_object = json.load(openfile)
        #check if old key present or not
        existing_data_keys=[]
        for key,value in json_object[0].items():
                existing_data_keys.append(key)
        if data not in existing_data_keys:
                print('Cannot Delete!!!, Key Not Present')
                #return False

        for i in json_object:
            del i[data]

        json_object = json.dumps(json_object, indent = 4)

        with open(self.filename+".json", "w") as outfile:
                outfile.write(json_object)
                outfile.close()
        print('Key Deleted')
        #return True


    def update_with_where(self,set_data,where_data):
        with open(self.filename+'.json', 'r') as openfile:
                json_object = json.load(openfile)

        existing_data_keys=[]
        for key,value in json_object[0].items():
                existing_data_keys.append(key)

        for key,value in set_data.items():
                if key not in list(json_object[0].keys()):
                        print('Cannot Update!!!, Set Key Not Present')
                        #return False

        for key,value in where_data.items():
                if key not in list(json_object[0].keys()):
                        print('Cannot Update!!!, Where Key Not Present')
                        #return False


        found=False
        for key,value in where_data.items():
                for i in json_object:
                        for j_key,j_value in i.items():
                                if key==j_key:
                                        #print(key,j_key,value,j_value)
                                        if value==j_value:
                                                #i[j_key]='hello_world'
                                                #print('found')
                                                found=True
                                                for s_key,s_value in set_data.items():
                                                        i[s_key]=s_value
        if found==False:
                print('Cannot Found Any Match In Data!!! ')
                #return False
                                                        

        json_object = json.dumps(json_object, indent = 4)

        with open(self.filename+".json", "w") as outfile:
                outfile.write(json_object)
                outfile.close()
        print('Data Updated')
        #return True


    def select_multiple(self,select_list):
        with open(self.filename+'.json', 'r') as openfile:
                json_object = json.load(openfile)

        for i in select_list:
                if i not in list(json_object[0].keys()):
                        print('Keys Not Present')
                        #return False

        main_data=[]

        for i in json_object:
            #print(i)
            temp_data={}
            for j in select_list:
                #print(j,i[j])
                #temp_data.append(i[j])
                temp_data[j]=i[j]
            main_data.append(temp_data)

        for i in main_data:
                print(i)
        #return True


    def select_multiple_with_where(self,select_list,where_dict):
        with open(self.filename+'.json', 'r') as openfile:
                json_object = json.load(openfile)

        for i in select_list:
                if i not in list(json_object[0].keys()):
                        print('Select Keys Not Present')
                        #return False

        for key,value in where_dict.items():
            if key not in list(json_object[0].keys()):
                print('Where Keys Not Present')
                #return False

        main_data=[]

        found=False
        #tempData=[]
        for key,value in where_dict.items():
            for item in json_object:
                if item[key]==value:
                    found=True
                    #tempData.append(item)
                    #item is our full json
                    temp_data={}
                    for i in select_list:
                        temp_data[i]=item[i]
                    main_data.append(temp_data)

        if found==False:
            print('Cannot Match Any Data With Where Condition!!! ')
            #return False

        for i in main_data:
            print(i)
                
        #return True



    def select_all(self):
        with open(self.filename+'.json', 'r') as openfile:
                json_object = json.load(openfile)

        for i in json_object:
            print(i)
                
        #return True



    def select_all_with_where(self,where_dict):
        with open(self.filename+'.json', 'r') as openfile:
                json_object = json.load(openfile)


        for key,value in where_dict.items():
            if key not in list(json_object[0].keys()):
                print('Where Keys Not Present')
                #return False

        main_data=[]

        found=False
        #tempData=[]
        for key,value in where_dict.items():
            for item in json_object:
                if item[key]==value:
                    found=True
                    #tempData.append(item)
                    #item is our full json

                    main_data.append(item)

        if found==False:
            print('Cannot Match Any Data With Where Condition!!! ')
            #return False

        for i in main_data:
            print(i)
                
        #return True






    '---------------------------------------------------------------------------------------------------------------------------------'

    def create_table_query(self,query):
        try:
            #print('create table called')
            table_name=query.split(' ')[2].split('(')[0]
            #print('table name is: ',table_name)

            create_table_json={}

            if '(' in query:
                starting_bracket_index=query.find('(')
                ending_bracket_index=query.find(')')
                create_table_data=query[starting_bracket_index+1:ending_bracket_index]
                #print('qqq',create_table_data)
                for i in create_table_data.split(','):
                    i=i.strip()
                    key=i.split()[0]
                    value=i.split()[1]
                    #print(key,value)
                    create_table_json[key]=value

                self.create([create_table_json])
                    
            else:
                print('Invalid Create Table Command, Please Use Below Command As Example')
                print('create table tablename(id text , name text , dob text)')
                #return False
        except:
            print('Invalid Create Table Command, Please Use Below Command As Example')
            print('create table tablename(id text , name text , dob text)')
            #return False





    def insert_table_query(self,query):
        try:

            first_opening_bracket=query.find('(')
            first_closing_bracket=query.find(')')
            if first_opening_bracket==-1 or first_closing_bracket==-1 or first_opening_bracket>first_closing_bracket:
                print('Invalid query')
                #return False
            #print(query[first_opening_bracket+1:first_closing_bracket])
            keys=query[first_opening_bracket+1:first_closing_bracket]
            keys=keys.split(',')


            if len(query.split('VALUES'))==2:
                #print('first if')
                temp_query=query.split('VALUES')[1]
            elif len(query.split('values'))==2:
                #print('second if')
                temp_query=query.split('values')[1]
            else:
                print('invalid query')
                #return False
                
            second_opening_bracket=temp_query.find('(')
            second_closing_bracket=temp_query.find(')')
            if second_opening_bracket==-1 or second_closing_bracket==-1 or second_opening_bracket>second_closing_bracket:
                print('Invalid query')
                #return False
                
            #print(temp_query[second_opening_bracket+1:second_closing_bracket])
            values=temp_query[second_opening_bracket+1:second_closing_bracket]
            values=values.split(',')

            new_dict = dict(zip(keys, values))
            #print(new_dict)

            self.insert(new_dict)
            
        except:
            print('Invalid Insert Table Command, Please Use Below Command As Example')
            print('INSERT INTO artists (name,age) valuesss(Bud,22);')
            #return False





    def alter_rename_query(self,query):
        try:
            old_column=query.split()[5:][0]
            new_column=query.split()[5:][2].replace(';','')

            self.alter_rename_column(old_column,new_column)
            
            #print(old_column,new_column)
        except:
            print('Invalid Alter Table Command, Please Use Below Command As Example')
            print('ALTER TABLE table_name RENAME COLUMN current_name TO new_name;')
            #return False


    def alter_add_column_query(self,query):
        try:
            new_column=query.split()[5:][0].replace(';','')
            self.alter_add_column(new_column)

        except:
            print('Invalid Alter Table Command, Please Use Below Command As Example')
            print('ALTER TABLE table_name ADD COLUMN COLUMN_NAME;')
            #return False


    def alter_drop_column_query(self,query):
        try:
            drop_column=query.split()[5:][0].replace(';','')
            self.delete(drop_column)

        except:
            print('Invalid Alter Table Command, Please Use Below Command As Example')
            print('ALTER TABLE table_name DROP COLUMN COLUMN_NAME;')
            #return False


    def update_with_where_query(self,query):
        try:
            temp_query_before_where=query.split('set')[1].split('where')[0].split(',')

            if len(temp_query_before_where)<1:
                print('Invalid Query,Please Use Below Command As Example')
                print('UPDATE tablename set id=23,name=abcd where name=pqrs')
                #return False
            
            set_data={}
            for i in temp_query_before_where:
                #print(i.split('='))
                set_data[i.split('=')[0].strip()]=i.split('=')[1].strip()
                
            #print(set_data)

            temp_query_after_where=query.split('set')[1].split('where')[1].split('=')
            if len(temp_query_before_where)!=2:
                print('Invalid Query,Please Use Below Command As Example')
                print('UPDATE tablename set id=23,name=abcd where name=pqrs')
                #return False

            where_json={temp_query_after_where[0].strip():temp_query_after_where[1].strip()}
            self.update_with_where(set_data,where_json)

        except:
            print('Invalid Query,Please Use Below Command As Example')
            print('UPDATE tablename set id=23,name=abcd where name=pqrs')
            #return False


    def select_multiple_query(self,query):
        try:
            data=query.split('select')[1].split('from')[0].split()[0].split(',')
            self.select_multiple(data)
        except:
            print('Invalid Query,Please Use Below Command As Example')
            print('select id,name,dob from tablename')
            #return False


    def select_multiple_with_where_query(self,query):
        try:
            data=query.split('select')[1].split('from')[0].split()[0].split(',')

            after_where=query.split('where')[1].split('=')
            if len(after_where)!=2:
                print('Invalid Query,Please Use Below Command As Example')
                print('select id,name,dob from tablename where name=sand')
                #return False

            where_dict={after_where[0].strip():after_where[1]}
            self.select_multiple_with_where(data,where_dict)

        except:
            print('Invalid Query,Please Use Below Command As Example')
            print('select id,name,dob from tablename where name=sand')
            #return False


    def select_all_with_where_query(self,query):
        try:
            after_where=query.split('where')[1].split('=')
            if len(after_where)!=2:
                    print('Invalid Query,Please Use Below Command As Example')
                    print('select * from tablename where name=sand')
                    #return False
            where_dict={after_where[0].strip():after_where[1]}

            self.select_all_with_where(where_dict)

        except:
            print('Invalid Query,Please Use Below Command As Example')
            print('select * from tablename where name=sand')
            #return False


    def select_all_query(self,query):
        self.select_all()










    def execute(self,query):
        query=' '.join(query.split())
    
        if query.split(' ')[0].lower()=='create':
            self.create_table_query(query)

        if query.split(' ')[0].lower()=='insert':
            self.insert_table_query(query)

        if query.split(' ')[0].lower()=='alter':
            if query.split()[3].lower()=='rename':
                self.alter_rename_query(query)

            elif query.split()[3].lower()=='add':
                if query.split()[4].lower()=='column':
                    self.alter_add_column_query(query)

            elif query.split()[3].lower()=='drop':
                if query.split()[4].lower()=='column':
                    self.alter_drop_column_query(query)
            else:
                print('Invalid Alter Command,Use Below As Example')
                print('ALTER TABLE table_name ADD/DROP COLUMN COLUMN_NAME;\nALTER TABLE table_name RENAME COLUMN current_name TO new_name;')
                #return False

        if query.split(' ')[0].lower()=='update' and query.split()[2].lower()=='set':
            self.update_with_where_query(query)

        if query.split()[0].lower()=='select':
            if 'where' in query:
                if '*' in query:
                    self.select_all_with_where_query(query)
                else:
                    self.select_multiple_with_where_query(query)
            else:
                if '*' in query:
                    self.select_all_query(query)
                else:
                    self.select_multiple_query(query)





def main():
    pass


if __name__ == "__main__":
    main()


                


#conn = connect("testing")

# conn.create([{'name':'','age':''}])

# conn.insert({'name':'abcd','age':'2345'})

# conn.alter_rename_column('name','full_name')

# conn.alter_add_column('height')

# conn.delete('height')

# conn.update_with_where({'full_name':'hello world','age':'2222222222222222'},{'age':'2345'}) 

# conn.select_multiple(['full_name','age'])

# conn.select_multiple_with_where(['full_name','age'],{'age':'2222222222222222','full_name':'hello world'})

#conn.select_all_with_where({'full_name':'hello'})

# conn.select_all()





# conn = connect("testfile")


# query="create table tablename(id text , name text , dob text)"
# conn.execute(query)


# print('--------------')
# query="INSERT INTO tablename (full_name,dob) valuesss(Bud,22);"
# conn.execute(query)

# print('--------------')
# query="ALTER TABLE table_name RENAME COLUMN full_name TO name;"
# conn.execute(query)


# print('--------------')
# query="ALTER TABLE table_name ADD COLUMN code;"
# conn.execute(query)


# print('--------------')
# query="ALTER TABLE table_name DROP COLUMN code;"
# conn.execute(query)


# print('--------------')
# query="UPDATE tablename set dob=23,name=sand where name=Bud"
# conn.execute(query)


# print('--------------')
# query="select id,name,dob from tablename"
# conn.execute(query)


# print('--------------')
# query="select id,name from tablename where name=sand"
# conn.execute(query)


# print('--------------')
# query="select * from tablename where name=sand"
# conn.execute(query)


# print('--------------')
# query="select * from tablename"
# conn.execute(query)













 
