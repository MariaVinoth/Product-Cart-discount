import urllib.request,json
import math

page_no = 1
#declaring constant variables as global
global url,id,c_products,c_price,c_collection,c_product_value,c_discount_value,c_pagination,c_total,c_per_page,c_discount_type,c_url_page,c_product,c_cart_value,c_id
url = "http://backend-challenge-fall-2018.herokuapp.com/carts.json?id="
c_products = "products"
c_price = "price"
c_collection = "collection"
c_product_value = "product_value"
c_discount_value = "discount_value"
c_pagination = "pagination"
c_total = "total"
c_per_page = "per_page"
c_discount_type = "discount_type"
c_url_page = "&page="
c_product = "product"
c_cart_value = "cart_value"
c_id = "id"

#function to calculate the discount when discount criteria is "collection"
def calc_collections(data,element_value,element,discount_value,total_after_discount,i):
    if len(data[c_products][i]) == 3 and data[c_products][i][element] == element_value:
        if data[c_products][i][c_price] - discount_value > 0:
            total_after_discount = total_after_discount + data[c_products][i][c_price] - discount_value
    else:
        total_after_discount += data[c_products][i][c_price]

    return total_after_discount

#function to calcuate the discount when discount criteria is for each product
def calc_product_value(data,element_value,discount_value,total_after_discount,i):
    if data[c_products][i][c_price] >= element_value:
        if data[c_products][i][c_price] - discount_value > 0:
            total_after_discount = total_after_discount + data[c_products][i][c_price] - discount_value
    else:
        total_after_discount += data[c_products][i][c_price]

    return total_after_discount

#function to calculate the discount when discount type is "product"
def calc_product(total_page,element_value, discount_value, element,page_no):
    total_after_discount = 0

    while page_no <= total_page:
        data = load_page(page_no)

        len_products = len(data[c_products])
        for i in range(len_products):
            if element == c_collection:
                total_after_discount = calc_collections(data,element_value,element,discount_value,total_after_discount,i)

            elif element == c_product_value:
                total_after_discount = calc_product_value(data, element_value, discount_value, total_after_discount, i)

            else:
                total_after_discount += data[c_products][i][c_price]
        page_no += 1

    if total_after_discount >= 0:
        return total_after_discount
    else:
        return 0


#function to calculate the discount when discount type is "cart"
def calc_cart(total_page,element_value,discount_value,page_no):
    cart_total = calc_total(total_page,page_no)
    if cart_total >= element_value:
        cart_total -= discount_value

    if cart_total >= 0:
        return cart_total
    else:
        return 0

#function to calculate total price of the cart
def calc_total(total_page,page_no):
    total_amount = 0
    while page_no <= total_page:
        data = load_page(page_no)
        len_products = len(data[c_products])
        for i in range(len_products):
            total_amount += data[c_products][i][c_price]
        page_no += 1
    return total_amount


#function to navigate to pages
def load_page(page_no):
    page = url +str(id)+c_url_page + str(page_no)
    response = urllib.request.urlopen(page)
    data = json.loads(response.read().decode('utf8'))
    return data


if __name__ == '__main__':
    s = input()
    inp = json.loads(s) #converting the input to json
    if c_collection in inp:
        element = c_collection
    elif c_product_value in inp:
        element = c_product_value
    else:
        element = c_cart_value
    id = inp[c_id]
    element_value = inp[element]
    discount_value = inp[c_discount_value]

    #to get the total pages
    temp_data = load_page(page_no)
    total_page = int(math.ceil(temp_data[c_pagination][c_total]/float(temp_data[c_pagination][c_per_page])))

    #calling respected function based on the discount type
    if inp[c_discount_type] == c_product:
        result = calc_product(total_page,element_value, discount_value, element,page_no)
    else:
        result = calc_cart(total_page,element_value, discount_value,page_no)

    total = calc_total(total_page,page_no=1)

    final_result ={"total_amount":total,"total_after_discount":result}
    print(json.dumps(final_result,indent=2)) #providing the output in json format

