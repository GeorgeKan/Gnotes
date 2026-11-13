from bottle import Bottle, template, redirect, request, response
from sqlmodel import Session, select, col, or_
import sqlalchemy

from dbutils.db import engine, create_db_and_tables
from dbutils.models import Tag, Package, Tutorial

app = Bottle()

#keep Root
@app.route('/')
def index():
    with Session(engine) as session:
        stmt = select(Package).limit(6)
        packages = list(session.exec(stmt))
        stmt = select(Tag).limit(9)
        tags = list(session.exec(stmt))
        return template('index', packages=packages, tags=tags)

#Tutorials main all
@app.route('/tutorials', method='GET')
def packages():
    with Session(engine) as session:
            stmt = select(Tutorial)
            tutorials = list(session.exec(stmt).all())
            return template('tutorials', tutorials=tutorials)

#Tutorials set filter
@app.route('/tutorials', method='POST')
def tutorials_filter():
    filter = str(request.forms.filter).strip()
    try:
        with Session(engine) as session:
            stmt = select(Tutorial).where(or_(Tutorial.name.contains(filter),Tutorial.desc.contains(filter)))
            tutorials = list(session.exec(stmt).all())
            return template('tutorials', tutorials=tutorials)
    except sqlalchemy.exc.NoResultFound:
        return template('tutorials', tutorials=[])


#Tutorials delete by id
@app.route('/tutorials/del', method='POST')
def tutorial_delete():
    data = request.json
    if not data or "id" not in data:
        response.status = 400
        return {'status':'error in request'}
    tutorialID = int(data['id'])
    with Session(engine) as session:
        tutorial = session.get(Tutorial, tutorialID)
        session.delete(tutorial)
        session.commit()
    return {"redirect":"/tutorials"}

#Tutorials post edited data
@app.route('/tutorials/edit', method='POST')
def tutorial_edited_data():
    id = int(request.forms.tutorialid)
    name = str(request.forms.tutorialname).strip()
    desc = str(request.forms.tutorialdesc).strip()
    url = str(request.forms.tutorialurl).strip()
    info = str(request.forms.tutorialinfo).strip()
    tag1 = int(request.forms.tag1)
    tag2 = int(request.forms.tag2)
    tag3 = int(request.forms.tag3)
    if len(name) < 3:
        response.set_cookie("msg", "Give valid Tutorial name. (Name more than 3 chars)")
        return redirect(f"/tutorials/edit/{id}")
    if len(desc) < 3:
        response.set_cookie("msg", "Give valid Tutorial Description.")
        return redirect(f"/tutorials/edit/{id}")
    if tag1 == -1 and tag2 == -1 and tag3 == -1:
        response.set_cookie("msg", "Give at leats one Tag for the tutorial")
        return redirect(f"/tutorials/edit/{id}")
    with Session(engine) as session:
        tutorial = session.get(Tutorial, id)
        stmt = select(Tag).where(col(Tag.id).in_([tag1,tag2,tag3]))
        tags = list(session.exec(stmt).all())
        tutorial.tags = tags
        tutorial.name = name
        tutorial.desc = desc
        tutorial.url = url
        tutorial.info = info
        session.add(tutorial)
        session.commit()
    redirect('/tutorials')



#tutorials select package to edit
@app.route('/tutorials/edit/<id:int>', method='GET')
def tutorials_edit_form(id:int):
    with Session(engine) as session:
            tutorial = session.get(Tutorial,id)
            if tutorial:
                stmt = select(Tag)
                tags = list(session.exec(stmt).all())
                msg = request.get_cookie("msg")
                response.set_cookie("msg", "")
                return template('edittutorial', tutorial=tutorial, tags=tags, msg=msg)
            else:
                redirect('/tutorials')

#Tutorial details
@app.route('/tutorials/<id:int>', method='GET')
def package_details(id):
    try:
        with Session(engine) as session:
            tutorial = session.get(Tutorial, id)
            return template('tutorialdetails', tutorial=tutorial)
    except sqlalchemy.exc.NoResultFound:
        return template('tutorialdetails', tutorial=Tutorial(name="Wrong Tutorial Name"))


#tutorials add form
@app.route('/tutorials/add', method='GET')
def tutorials_add_form():
    session = Session(engine)
    stmt = select(Tag)
    tags = list(session.exec(stmt).all())
    session.close()
    tags.sort(key=lambda x: x.name)
    msg = request.get_cookie("msg")
    response.set_cookie("msg", "")
    return template('addtutorial', msg=msg, tags=tags)

#tutorial add post data
@app.route('/tutorials/add', method='POST')
def tutorials_add_packages():
    name = str(request.forms.tutorialname).strip()
    desc = str(request.forms.tutorialdesc).strip()
    url = str(request.forms.tutorialurl).strip()
    info = str(request.forms.tutorialinfo).strip()
    tag1 = int(request.forms.tag1)
    tag2 = int(request.forms.tag2)
    tag3 = int(request.forms.tag3)
    if len(name) < 3:
        response.set_cookie("msg", "Give valid Tutorials name. (Name more than 3 chars)")
        return redirect("/tutorials/add")
    if len(desc) < 3:
        response.set_cookie("msg", "Give valid Tutorial Description.")
        return redirect("/tutorials/add")
    if tag1 == -1 and tag2 == -1 and tag3 == -1:
        response.set_cookie("msg", "Give at leats one Tag for the tutorial")
        return redirect("/tutorials/add")
    session = Session(engine)
    stmt = select(Tag).where(col(Tag.id).in_([tag1,tag2,tag3]))
    tags = list(session.exec(stmt).all())
    newPackage = Tutorial(name=name,desc=desc,url=url,info=info, tags=tags)
    try:
        session.add(newPackage)
        session.commit()
        session.refresh(newPackage)
        session.close()
    except sqlalchemy.exc.IntegrityError:
            session.close()
            response.set_cookie("msg", f"Tutorial {name} already exists.")
            return redirect("/tutorials/add")
    return redirect('/tutorials')


#Packages main all
@app.route('/packages', method='GET')
def packages():
    with Session(engine) as session:
            stmt = select(Package)
            packages = list(session.exec(stmt).all())
            return template('packages', packages=packages)

#Packages set filter
@app.route('/packages', method='POST')
def package_filter():
    filter = str(request.forms.filter).strip()
    try:
        with Session(engine) as session:
            stmt = select(Package).where(or_(Package.name.contains(filter),Package.desc.contains(filter)))
            packages = list(session.exec(stmt).all())
            return template('packages', packages=packages)
    except sqlalchemy.exc.NoResultFound:
        return template('packages', package=[])    

#packages post edited data
@app.route('/packages/edit', method='POST')
def package_edited_data():
    id = int(request.forms.packageid)
    name = str(request.forms.packagename).strip()
    desc = str(request.forms.packagedesc).strip()
    url = str(request.forms.packageurl).strip()
    info = str(request.forms.packageinfo).strip()
    tag1 = int(request.forms.tag1)
    tag2 = int(request.forms.tag2)
    tag3 = int(request.forms.tag3)
    if len(name) < 3:
        response.set_cookie("msg", "Give valid Package name. (Name more than 3 chars)")
        return redirect(f"/packages/edit/{id}")
    if len(desc) < 3:
        response.set_cookie("msg", "Give valid Package Description.")
        return redirect(f"/packages/edit/{id}")
    if tag1 == -1 and tag2 == -1 and tag3 == -1:
        response.set_cookie("msg", "Give at leats one Tag for the package")
        return redirect(f"/packages/edit/{id}")
    with Session(engine) as session:
        package = session.get(Package, id)
        stmt = select(Tag).where(col(Tag.id).in_([tag1,tag2,tag3]))
        tags = list(session.exec(stmt).all())
        package.tags = tags
        package.name = name
        package.desc = desc
        package.url = url
        package.info = info
        session.add(package)
        session.commit()
    redirect('/packages')


#packages select package to edit
@app.route('/packages/edit/<id:int>', method='GET')
def package_edit_form(id:int):
    with Session(engine) as session:
            package = session.get(Package,id)
            if package:
                stmt = select(Tag)
                tags = list(session.exec(stmt).all())
                msg = request.get_cookie("msg")
                response.set_cookie("msg", "")
                return template('editpackage', package=package, tags=tags, msg=msg)
            else:
                redirect('/packages')

#Packages delete by id
@app.route('/packages/del', method='POST')
def package_delete():
    data = request.json
    if not data or "id" not in data:
        response.status = 400
        return {'status':'error in request'}
    packageID = int(data['id'])
    with Session(engine) as session:
        package = session.get(Package, packageID)
        session.delete(package)
        session.commit()
    return {"redirect":"/packages"}

#Packages details
@app.route('/packages/<packagename>', method='GET')
def package_details(packagename):
    try:
        with Session(engine) as session:
            stmt = select(Package).where(Package.name == packagename.strip())
            package = session.exec(stmt).one()
            return template('packagedetails', package=package)
    except sqlalchemy.exc.NoResultFound:
        return template('packagedetails', package=Package(name="Wrong Package Name"))

#packages add form
@app.route('/packages/add', method='GET')
def packages_add_form():
    session = Session(engine)
    stmt = select(Tag)
    tags = list(session.exec(stmt).all())
    session.close()
    tags.sort(key=lambda x: x.name)
    msg = request.get_cookie("msg")
    response.set_cookie("msg", "")
    return template('addpackage', msg=msg, tags=tags)

#Packages add post data
@app.route('/packages/add', method='POST')
def packages_add_packages():
    name = str(request.forms.packagename).strip()
    desc = str(request.forms.packagedesc).strip()
    url = str(request.forms.packageurl).strip()
    info = str(request.forms.packageinfo).strip()
    tag1 = int(request.forms.tag1)
    tag2 = int(request.forms.tag2)
    tag3 = int(request.forms.tag3)
    if len(name) < 3:
        response.set_cookie("msg", "Give valid Package name. (Name more than 3 chars)")
        return redirect("/packages/add")
    if len(desc) < 3:
        response.set_cookie("msg", "Give valid Package Description.")
        return redirect("/packages/add")
    if tag1 == -1 and tag2 == -1 and tag3 == -1:
        response.set_cookie("msg", "Give at leats one Tag for the package")
        return redirect("/packages/add")
    session = Session(engine)
    stmt = select(Tag).where(col(Tag.id).in_([tag1,tag2,tag3]))
    tags = list(session.exec(stmt).all())
    newPackage = Package(name=name,desc=desc,url=url,info=info, tags=tags)
    try:
        session.add(newPackage)
        session.commit()
        session.refresh(newPackage)
        session.close()
    except sqlalchemy.exc.IntegrityError:
            session.close()
            response.set_cookie("msg", f"Package {name} already exists.")
            return redirect("/packages/add")
    return redirect('/packages')


#keep Tags
@app.route('/tags', method='GET')
def tags():
    with Session(engine) as session:
        stmt = select(Tag)
        tags = list(session.exec(stmt).all())
        return template('tags', tags=tags)

#keep Tags
@app.route('/tags', method='POST')
def filter_tags():
    filter = str(request.forms.filter).strip()
    try:
        with Session(engine) as session:
            stmt = select(Tag).where(Tag.name.contains(filter))
            tags = list(session.exec(stmt).all())
            return template('tags', tags=tags)
    except sqlalchemy.exc.NoResultFound:
        return template('tags', tags=[]) 

#keep Tags
@app.route('/tags/<tagname>')
def tag_details(tagname):
    try:
        with Session(engine) as session:
            stmt = select(Tag).where(Tag.name == tagname.strip().lower())
            tag = session.exec(stmt).one()
            return template('tagdetails', tag=tag)
    except sqlalchemy.exc.NoResultFound:
        return template('tagdetails', tag=Tag(name="Wrong Tag Name", packages=[]))
    
#keep Tags
@app.route('/tags/add', method='GET')
def tags_add_form():
    msg = request.get_cookie("msg")
    response.set_cookie("msg", "")
    return template('addtag', msg=msg)

#keep Tags
@app.route('/tags/add', method='POST')
def tags_add_tag():
    name = str(request.forms.tagname)
    name = name.strip().lower()
    if not name:
            response.set_cookie("msg", "Not Tag Inserted.")
            return redirect("/tags/add")
    try:
        session = Session(engine)
        newTag = Tag(name=name)
        session.add(newTag)
        session.commit()
        session.refresh(newTag)
        session.close()
    except sqlalchemy.exc.IntegrityError:
            session.close()
            response.set_cookie("msg", f"Tag {name} already exists.")
            return redirect("/tags/add")
    redirect("/tags")


def main():
    create_db_and_tables()
    app.run(host='0.0.0.0', port=8080, reloader=True, debug=True)

if __name__ == '__main__':
    main()