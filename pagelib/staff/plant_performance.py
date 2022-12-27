import pandas as pd
import streamlit as st
import numpy as np
import mysql.connector

def plant_performance():
    st.title("Plant Performance")
    st.header("""\n
    This page has three categories of features to show\n
    1. Province sales ranking:\n
    Under this function, you can select multiple provinces by themselves. The names of the six chips with the highest REVENUE under the selected provinces will be displayed in the form of a table\n
    2. Monthly REVENUE overview:\n
    Under this function, you can see the monthly revenue change of the company on the line chart\n
    3. Order completion:\n
    Under this function, you can see the change in the number of orders received and completed by the company each month on the AREA chart\n
    """)


    tab1, tab2, tab3= st.tabs(["Province sales ranking", "Monthly REVENUE Overview","Order completion"])
    with tab1:
        cnx1 = mysql.connector.connect(
            host="123.60.157.95",
            port=3306,
            user="root",
            password="csc123456@",
            database="project")
        cur1 = cnx1.cursor()
        cur1.execute("""
                    select distinct province
                    from user; 
                    """)
        All_p_Option = cur1.fetchall()
        Select_Box = []
        for i in All_p_Option:
            Select_Box.append(i[0])

        selected = st.multiselect(
            'Select the province you want to check:',
            Select_Box,
            ['Guangdong'] 
        )
        province = ""
        for i in selected:
            province += "'"
            province += i
            province += "'"
            province += ','
        province = province[:-1]

        cnx2 = mysql.connector.connect(
            host="123.60.157.95",
            port=3306,
            user="root",
            password="csc123456@",
            database="project")
        cur2 = cnx2.cursor()
        if province != "":
            cur2.execute("""
                        select u.province, c.chip_name as ChipName,sum(p.budget) as revenue
                        from user AS u natural join package AS p, chip AS c
                        where p.package_id=c.package_id and province in (%s)
                        group by c.chip_name
                        order by sum(p.budget) desc; 
                        """%(province))

            df1 = pd.DataFrame(
                cur2.fetchmany(6),
                columns=["Province", "Chip Name","Revenue"])
            st.table(df1)
        else:
            st.text("Please select at least one province!")
    with tab2:    
        cnx3 = mysql.connector.connect(
            host="123.60.157.95",
            port=3306,
            user="root",
            password="csc123456@",
            database="project")
        cur3 = cnx3.cursor()
        cur3.execute("""
                    select sum(p.budget) as revenue, DATE_FORMAT(p.create_time,'%Y-%m-%d') as create_time
                    from user as u, package as p
                    where u.province in ('Guangdong','Hubei')
                    GROUP BY MONTH(p.create_time)
                    ORDER BY p.create_time asc
                    """)
        column=[col[0] for col in cur3.description]
        data = cur3.fetchall()
        df2=pd.DataFrame(list(data),columns=column)
        df2['create_time'] = pd.to_datetime(df2['create_time'])
        df2 = df2.set_index('create_time')
        df2['revenue'] = df2['revenue'].astype(float)
        st.line_chart(df2)

    with tab3:
        cnx4 = mysql.connector.connect(
            host="123.60.157.95",
            port=3306,
            user="root",
            password="csc123456@",
            database="project")
            
        cur4 = cnx4.cursor()
        cur4.execute('''select Date, count(*) as finish_num
                        from (select DATE(p.CREATE_TIME) as date, s.state_name as status
                        from package as p natural join state as s) as joint
                        where Status='Finished'
                        GROUP BY MONTH(Date)
                        ORDER BY Date asc''')
        column=[col[0] for col in cur4.description]
        data = cur4.fetchall()
        finished=pd.DataFrame(list(data),columns=column)
    

        cnx5 = mysql.connector.connect(
            host="123.60.157.95",
            port=3306,
            user="root",
            password="csc123456@",
            database="project")

        cur5=cnx5.cursor()
        cur5.execute('''select Date, count(*) as all_num
                        from (select DATE(p.CREATE_TIME) as date, s.state_name as status
                        from package as p natural join state as s) as joint
                        GROUP BY MONTH(Date)
                        ORDER BY Date asc''')
        column=[col[0] for col in cur5.description]
        data = cur5.fetchall()
        all=pd.DataFrame(list(data),columns=column)

        all['Finished num'] = finished['finish_num'].values
        all['date'] = pd.to_datetime(all['date'])
        all = all.set_index('date')
        st.area_chart(all)
    cnx1.close()
    cnx2.close()
    cnx3.close()
    cnx4.close()
    cnx5.close()
