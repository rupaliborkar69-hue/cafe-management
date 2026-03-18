from flask import *
import sqlite3
import os

app=Flask(__name__)
app.config["UPLOAD_FOLDER"]="c:/Users/Rupali Borkar/OneDrive/Desktop/cafe_management/static/images"
app.secret_key="rstpava"
menu_data={
        "coffee":80,
        "tea":30,
        "sandwitch":120,
        "burger":150,
        "cake":90

    }
@app.route("/")
def index():
        return render_template("index.html")

@app.route("/menu")
def menu():
        return render_template("menu.html",menu=menu_data)

@app.route("/login")
def login():
      return render_template("login.html")
    

@app.route("/bill", methods=["POST"])
def bill():

        items = []
        total = 0

        for item, price in menu_data.items():
            qty = request.form.get(item)

            if qty and int(qty) > 0:
                qty = int(qty)
                cost = qty * price
                total += cost

                items.append({
                    "name": item,
                    "qty": qty,
                    "cost": cost
                })

        return render_template("bill.html", items=items, total=total)

@app.route("/registration")
def registration():
            return render_template("registration.html")


@app.route("/saveform", methods=["POST"])
def saveform():
        if request.method=="POST":
            fn=request.form["fullname"]
            em=request.form["email"]
            cn=request.form["phone_number"]
            ad=request.form["address"]
            ps=request.form["password"]
            cp=request.form["confirm_password"]

            con=sqlite3.connect("cm.db")
            c=con.cursor()
            c.execute("insert into registration1(fullname,email,phone_number,address,password,confirm_password)values(?,?,?,?,?,?)",(fn,em,cn,ad,ps,cp))
            con.commit()
            con.close()

            return redirect(url_for("menu"))
        else:
            return  "failed"
@app.route("/viewdata")
def viewdata():
        con=sqlite3.connect("cm.db")
        c=con.cursor()
        c.execute("select * from registration1 ")
        data=c.fetchall()
        print("DATA:", data)
        
        con.close() 
        return render_template("viewdata.html",data=data)

@app.route("/deletedata/<int:id>")
def deletedata(id):
       con=sqlite3.connect("cm.db")
       c=con.cursor()
       c.execute("delete from registration1 where id=?",[id])
       
       con.commit()
     
       return redirect(url_for("viewdata"))

@app.route("/profileupdate/<int:id>",methods=["GET","POST"])
def profileupdate(id):
        if request.method=="POST":
           fn=request.form["fullname"]
           em=request.form["email"]
           cn=request.form["phone_number"]
           ad=request.form["address"]
           ps=request.form["password"]
           cp=request.form["confirm_password"]

           con=sqlite3.connect("cm.db") 
           c=con.cursor()
           c.execute("update registration1 set fullname=?, email=?, phone_number=?, address=?, password=?, confirm_password=? where id=?",(fn,em,cn,ad,ps,cp,id)) 
           con.commit()
           con.close()
           return redirect(url_for("viewdata"))
        
        con=sqlite3.connect("cm.db")
        c=con.cursor()
        c.execute("select * from registration1 where id=?",(id,))
        data=c.fetchone()
        con.close()
        return render_template("profileupdate.html",data=data)

@app.route("/logincheck",methods=["POST","GET"])
def logincheck():
       if request.method=="POST":
          em=request.form["email"]
          ps=request.form["password"]
          con=sqlite3.connect("cm.db") 
          c=con.cursor()
          c.execute("select * from registration1 where email=? and password=?",(em,ps))
          data=c.fetchall()
          con.commit()
          con.close()
          if data:
             session["username"]=em
        #   return redirect(url_for("dashboard",data=data))
             return "<script>window.alert('login successfully');window.location.href='/dashboard'</script>"
          else:
            return "<script>window.alert('login failed'); window.location.href='/login'</script>"
       else:
          return render_template("login.html")
      
@app.route("/dashboard") 
def dashboard():
      if session.get('username') is not None:
        em=session.get('username')
        con=sqlite3.connect("cm.db")
        c=con.cursor()
        c.execute("select * from registration1 where email=?",[em])
        data=c.fetchone()
        return render_template("dashboard.html",data=data) 
      else:
            return redirect(url_for("login"))
      

@app.route("/logout")   
def logout():
      session.pop('username',None)   
      return redirect(url_for("login"))


@app.route("/fileupload")
def fileupload():
      return render_template("fileupload.html")


@app.route("/filesave",methods=["POST"])
def filesave():
      if request.method=="POST":
         ph=request.files["photo"]
        #  ph.save(ph.filename)
         ph.save(os.path.join(app.config["UPLOAD_FOLDER"],ph.filename))
         return "upload successfully"
      else:
            return "failed"
      

    

         

       
        

if __name__=="__main__":
         app.run(debug=True)













