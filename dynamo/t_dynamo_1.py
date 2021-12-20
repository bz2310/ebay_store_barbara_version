import json
import dynamodb as db
import copy
import uuid


def t1():

    res = db.get_item("reviews",
                      {
                          "comment_id": "411d2caf-975f-4475-b5c8-e3c46384777e"
                      })
    print("Result = \n", json.dumps(res, indent=4, default=str))


def t2():

    res = db.find_by_template("reviews", {
        "product_no" : "2"
    })
    print("Result = \n", json.dumps(res, indent=4, default=str))


def t3():
    table_name = "reviews"
    commenter = "bar"
    response = "Thanks for the review!"
    res = db.add_response(table_name, "411d2caf-975f-4475-b5c8-e3c46384777e", commenter,
                         response)
    print("t3 -- res = ", json.dumps(res, indent=3))


def t4():
    tag = 'Sports'
    res = db.find_by_tag(tag)
    print("Comments with tag 'science' = \n", json.dumps(res, indent=3, default=str))


def t5():
    print("Do a projection ...\n")
    res = db.do_a_scan("comments",
                       None, None, "#c, comment_id", {"#c": "comment"})
    print("Result = \n", json.dumps(res, indent=4, default=str))


def t6():

    comment_id = "411d2caf-975f-4475-b5c8-e3c46384777e"
    original_comment = db.get_item("reviews",{"comment_id": comment_id})
    #original_version_id = original_comment["version_id"]

    new_comment = copy.deepcopy(original_comment)

    try:
        res = db.write_comment_if_not_changed(original_comment, new_comment)
        print("First write returned: ", res)
    except Exception as e:
        print("First write exception = ", str(e))

    try:
        res = db.write_comment_if_not_changed(original_comment, new_comment)
        print("Second write returned: ", res)
    except Exception as e:
        print("Second write exception = ", str(e))

def t7():
    res=db.put_comment("reviews", "test", "Awesome product!", "2")
    print("Result = \n", json.dumps(res, indent=4, default=str))

# def t8():



# t1()
# t2()
# t3()
# t4()
# t5()
t6()
# t7()
# t3()

