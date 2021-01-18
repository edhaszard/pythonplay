import msal
import requests
import json
import pymssql

client_id = '41830863-3f79-4c6e-afb4-b663b432dca5'
tenant_id = '35558aca-3637-44e9-8cc7-393f0482cb28'
client_secret = 'mMwua1ft-20nME1_hkZ~~x-ZBHd6G1XkHv'
#sqlserver = "172.22.0.70"
#sqldatabase = "Payglobal"
#sqluserid = "AWS_Glue_Login_SQLAuthentication_PG"
#sqlpassword = "kG2zonHQ9llBmfl503mLHyugwSbOliIO"
#sqlport = "1433"
 
#def update_pg_from_ad():
    # get paygobal users to check
#    def get_pg_users():
#        conn = pymssql.connect(sqlserver, sqluserid, sqlpassword, sqldatabase)
#        cursor = conn.cursor()
#        cursor.execute(
#            "select e.employeecode, coalesce (e.workemail, '') workemail, e.employeeid from dbo.employee e "
#            "where e.employeecode = '915652' and coalesce (e.terminationdate, '9999-12-31') > getdate()")
#        return cursor.fetchall()

    # get graph api token
def get_token(client_id, tenant_id, client_secret):
        scope = ["https://graph.microsoft.com/.default"]
        app = msal.ConfidentialClientApplication(client_id,
                                                 authority='https://login.microsoftonline.com/{}'.format(tenant_id),
                                                 client_credential=client_secret
                                                 )
        result = app.acquire_token_silent(scopes=scope, account=None)
        if not result:
            result = app.acquire_token_for_client(scopes=scope)
        return result['access_token']

    # get current aad user list
    def get_ad_users(token):
        ad_user_list = []
        stop = False
        ad_initial = json.loads(requests.get(
            "https://graph.microsoft.com/v1.0/users?$select=id,email,userPrincipalName,employeeId,jobTitle,department",
            headers={'Authorization': 'Bearer ' + token}).content)
        for u in ad_initial['value']: ad_user_list.append(u)
        next_link = ad_initial['@odata.nextLink']

        while not stop:
            try:
                ad_details = json.loads(requests.get(next_link, headers={'Authorization': 'Bearer ' + token}).content)
                for u in ad_details['value']: ad_user_list.append(u)

                # ad_user_list.append(ad_details['value'])
                next_link = ad_details['@odata.nextLink']
            except KeyError:
                stop = True
        # print(ad_user_list)
        return ad_user_list

    # compare
#    def check_pg_emails(ad_users, pg_users):
#        updates = []
#        for pg_user in pg_users:
#            employee_code = pg_user[0]
#            workemail = pg_user[1]
            # print(workemail)

#            try:
#                for user in ad_users:
#                    ad_empno = user['employeeId']
#                    if ad_empno is not None:
#                        ad_email = user['userPrincipalName']
#                        if ad_empno == employee_code and workemail.upper() != ad_email.upper():
#                            updates.append({'employeecode': ad_empno, 'workemail': ad_email, 'employeeid': pg_user[2], 'currentemail': workemail})
#            except TypeError:
#                ad_empno = None
#        return updates

#    def update_pg_email(user_updates):
#        conn = pymssql.connect(sqlserver, sqluserid, sqlpassword, sqldatabase)
#        cursor = conn.cursor()
#        for user in user_updates:
#            sql = "update dbo.Employee set WorkEmail = '{}' where EmployeeCode = '{}'".format(user["workemail"],user["employeecode"])
#            sql_audit_log = """
#            Insert into AuditLog (ChangeDate, ChangeTime, UserName, Field, Before, After, Event, TableName, EmployeeCode, RecordID)
#            values(CONVERT(datetime, datediff(day,0,getdate())) ,ABS(CAST(CONVERT(datetime,GETDATE()) as float)) - FLOOR(abs(CAST(CONVERT(datetime,GETDATE()) as float))),
#            'AIRFLOW', 'WORKEMAIL', '{}', '{}','E','EMPLOYEE', '{}', '{}')
#           """.format(user["currentemail"] ,user["workemail"],user["employeecode"],user["employeeid"])
#            print("Executing",sql_audit_log)
#            print("Executing",sql)
            # cursor.execute(sql)
            # conn.commit()
            # cursor.execute(sql_audit_log)
            # conn.commit()


    token = get_token(client_id, tenant_id, client_secret)
#    ad_users = get_ad_users(token=token)
    pg_users = get_pg_users()
#    user_updates = check_pg_emails(ad_users=ad_users, pg_users=pg_users)
#    update_pg_email(user_updates = user_updates)


update_pg_from_ad()

