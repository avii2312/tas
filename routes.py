from app import app,db
from flask import request, jsonify
from models import Member


@app.route("/api/members",methods=["GET"])
def get_members():
 members = Member.query.all()
 result = [member.to_json() for member in members]
 return jsonify(result)

@app.route("/api/members",methods=["POST"])
def create_member():
  try:
    data = request.json
    
    required_fields=["name", "role", "description","gender"]
    for field in required_fields:
      if field not in data:
        return jsonify({"error":f'Missing details:{field}'}),400

    name = data.get("name")
    role = data.get("role")
    description = data.get("description")
    gender = data.get("gender")
  
  
    if gender == "male":
     img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
    elif gender =="female":
      img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
    else:
     img_url = None

    new_member = Member(name=name, role=role, description=description, gender=gender, img_url=img_url)
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"msg":"New Member is created"}),201
  except Exception as e:
    db.session.rollback()
    return jsonify({"error":str(e)}),500

@app.route("/api/members/<int:id>",methods=["DELETE"])
def delete_member(id):
  try:
    member = Member.query.get(id)
    if member is None:
      return jsonify({"error":"Member not found"}),404
    
    db.session.delete(member)
    db.session.commit()
    return jsonify({"msg":"Member deleted"}),200
  except Exception as e:
    db.session.rollback()
    return jsonify({"error":str(e)}),500
  
@app.route("/api/members/<int:id>",methods=["PATCH"])
def update_member(id):
  try:
    member = Member.query.get(id)
    if member is None:
      return jsonify({"error":"Member not found"}),404
    data = request.json
    
    member.name = data.get("name",member.name)
    member.role = data.get("role",member.role)
    member.description = data.get("description",member.description)
    member.gender = data.get("gender",member.gender)
    
    db.session.commit()
    return jsonify(member.to_json()),200
    
  except Exception as e:
    db.session.rollback()
    return jsonify({"error":str(e)}),500
 