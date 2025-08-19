from database.DB_connect import DBConnect
from model.Product import Product


class DAO():

    @staticmethod
    def getColors():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select Product_color 
                        from go_products gp 
                        group by Product_color """
            cursor.execute(query)
            for row in cursor:
                res.append(row["Product_color"])
            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getNodes(color):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select Product_number, Product, Product_color from go_products gp 
                        where Product_color = %s"""
            cursor.execute(query, (color,))
            for row in cursor:
                res.append(Product(**row))
            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getEdges(year, color):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()

            query = """select pn1, pn2, pc1, d1, rc1, count(*) as weight
                        from (select * 
                        from(select pn1, pn2, pc1, d1, rc1 
                        from((select gp.Product_number as pn1, gp.Product_color as pc1, gds.Date as d1, gds.Retailer_code as rc1 
                        from go_daily_sales gds 
                        join go_products gp 
                        on gp.Product_number = gds.Product_number 
                        where gp.Product_color  = %s and year(gds.Date) = %s) tab1
                        join (select  gp2.Product_number as pn2, gp2.Product_color as pc2, gds2.Date as d2, gds2.Retailer_code as rc2
                        from go_daily_sales gds2
                        join go_products gp2
                        on gp2.Product_number = gds2.Product_number 
                        where gp2.Product_color  = %s and year(gds2.Date) = %s) tab2
                        on tab1.rc1 = tab2.rc2
                        and tab1.d1 = tab2.d2)
                        where tab1.pn1 < tab2.pn2) mytab
                        group by mytab.d1, mytab.pn1, mytab.pn2) deftab
                        group by deftab.pn1, deftab.pn2"""
            cursor.execute(query, (color, year, color, year))
            for row in cursor:
                res.append(row)
            cursor.close()
            cnx.close()
        return res
