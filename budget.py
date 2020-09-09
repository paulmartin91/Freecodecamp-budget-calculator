class Category:
  
  def __init__(self, name):
    self.name = name
    self.ledger = list()
    self.balance = 0

  def __str__(self):
    number_of_stars = int((30-(len(self.name)))/2)
    headline = "*"*number_of_stars+self.name+"*"*number_of_stars+"\n"
    ledger_items = ""
    total = 0
    for ledger_item in self.ledger:
      total = total + ledger_item["amount"]
      amount_to_string = str("{:.2f}".format(ledger_item["amount"]))
      amount_to_string_shortened = amount_to_string[0:7]
      ledger_items += ledger_item["description"][0:23] + " " * (30 - (len(amount_to_string_shortened) + len(ledger_item["description"][0:23]))) + amount_to_string[0:7] + "\n"
    return headline+ledger_items + "Total: " + str(total)

  def deposit(self, amount, description=""):
    self.balance = self.balance + amount
    self.ledger.append({"amount": round(amount, 2), "description": description})

  def withdraw(self, amount, description=""):
    if (not self.check_funds(amount)):
      return False
    else:
      self.balance = self.balance - amount
      self.ledger.append({"amount": -round(amount, 2), "description": description})
      return True

  def get_balance(self):
    return self.balance

  def transfer(self, amount, destination_category):
    if (not self.check_funds(amount)):
      return False
    else:
      self.withdraw(amount, "Transfer to "+destination_category.name)
      destination_category.deposit(amount, "Transfer from "+self.name)
      return True

  def check_funds(self, amount):
    if (self.balance - amount < 0): 
      return False
    else: 
      return True


def create_spend_chart(list_of_categories):
  spending_hist = dict()
  total_spent = 0
  graph = "Percentage spent by category\n"
  for category in list_of_categories:
    spending_hist[category.name] = 0
    for ledger_entry in category.ledger:
      if (ledger_entry["amount"] < 0):
        #print(category.name, ledger_entry["amount"])
        spending_hist[category.name] += ledger_entry["amount"]
        total_spent += ledger_entry["amount"]

  #print(total_spent)
  #print(spending_hist)

  x_axis = 100
  longest_category_name = 0

  while x_axis >= 0:
    if (x_axis == 100): line = str(x_axis) + "|"
    elif (x_axis == 0): line = "  " + str(x_axis) + "|"
    else: line = " " + str(x_axis) + "|"
    for name, total in spending_hist.items():
      if (len(name) > longest_category_name): longest_category_name = len(name)
      if (total == 0): current_category = 0
      else: current_category = (100 * total / total_spent) - (100 * total / total_spent)%10
      #print(current_category)
      if (current_category >= x_axis):
        line += " o "
      else:
          line += "   "
    #print(line)
    graph += line + " \n"
    x_axis -= 10

  graph+= "    -"+("---"*len(spending_hist))
  counter = 0

  while counter < longest_category_name:
    #print(longest_category_name)
    line = []
    for name, total in spending_hist.items():
      if len(name) > counter:
        #print("name = ", name, "length of name = ", len(name), "counter = ", counter)
        line.append(name[counter])
      else:
        line.append(" ")
    counter += 1
    graph += "\n     "+"  ".join(line) + "  "

  

  return graph