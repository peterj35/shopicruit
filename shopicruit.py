# Written in Python, tested with 3.5.1.
# Noticed that Shopify offered a similar task involving lamps
# and wallets in prior years instead of keyboards and computers,
# so this is a somewhat general solution for prices and weights.

import requests

def main():
    base_url = "http://shopicruit.myshopify.com/products.json?page="
    # Adjust these tags according to the products you want to combinate
    tag_1 = "Keyboard"
    tag_2 = "Computer"
    list_1 = []
    list_2 = []
    combinated_list = []
    total_weight = 0
    total_cost	 = 0

    # Iterate through the multiple json pages and extract products,
    # according to their tags
    for page_no in range(1, 6):
        url = base_url + str(page_no)
        extract_products(url, list_1, tag_1)
        extract_products(url, list_2, tag_2)

    # Download sorted lists of items with tag 1 and tag 2,
    # and output them to text files.
    # list_1 = sorted(list_1, key=get_price)
    # list_2 = sorted(list_2, key=get_price)
    # with open(tag_1+'s.txt', 'w', encoding='utf-8') as output1:
    #     for item in list_1:
    #         output1.write("%s\n" % item)
    # with open(tag_2+'s.txt', 'w', encoding='utf-8') as output2:
    #     for item in list_2:
    #         output2.write("%s\n" % item)

    # Create the combinated_list, with the format:
    # [[item1, item2], cost, weight]
    for i in range(len(list_1)):
        for k in range(len(list_2)):
            combination = combinate(list_1[i], list_2[k])
            combinated_list.append([combination, 
                get_combination_cost(combination), 
                get_combination_weight(combination)])
            total_cost += get_combination_cost(combination)
            total_weight += get_combination_weight(combination)

    combinated_list = sorted(combinated_list, key=get_price)

	# print(total_weight)
	# print(combinated_list)

    # Write variations list to 'shoppinglist.txt'
    with open('shoppinglist.txt', 'w', encoding='utf-8') as output:
        output.write(
            ("Your Shopicruit %ss and %ss "+
            "shopping list.\nTotal weight is: %s grams.\nTotal "+
            "cost is: %.2f dollars.\n\n") 
            % (tag_1, tag_2, total_weight, total_cost)
        )
        for item in combinated_list:
            output.write("%s\n" % item)

    print("Success! Check shoppinglist.txt.")

# Sends a request to the url, returns a list corresponding
# to the tag argument provided, extracting variants.
# Returns a list of matched tags with the format:
# [Variants:TITLE TITLE, by VENDOR, Variants:PRICE, Variants:GRAMS]
def extract_products(url, alist, tag):
    r = requests.get(url)
    products_json = r.json()['products']
    for i in range(len(products_json)):
        entries = products_json[i]
        if tag in entries['tags']:
            for variants in entries['variants']:
                alist.append([str(variants['title'])+' '+
                    str(entries['title'])+', by '+
                    (entries['vendor']), float(variants['price']), 
                    variants['grams']])
    return alist

def combinate(list1, list2):
    return([list1, list2])

def get_combination_cost(combolist):
    return combolist[0][1] + combolist[1][1]

def get_combination_weight(combolist):
    return combolist[0][2] + combolist[1][2]

def get_price(item):
    return item[1]
    
if __name__ == '__main__':
    main()