import pickle
import datetime

class BudgetingBackend:
    def __init__(self, filename='budget_data.pkl'):
        self.filename = filename
        self.categories = self.load_data()

    def add_category(self, name, category_type, limit):
        if name in self.categories:
            return False, "This category already exists."
        self.categories[name] = {'type': category_type, 'limit': limit, 'expenses': []}
        return True, "Category added successfully."

    def update_category(self, old_name, new_name, category_type, limit):
        if old_name not in self.categories:
            return False, "Category does not exist."
        if new_name in self.categories and old_name != new_name:
            return False, "New category name already exists."
        self.categories[new_name] = self.categories.pop(old_name)
        self.categories[new_name]['type'] = category_type
        self.categories[new_name]['limit'] = limit
        return True, "Category updated successfully."

    def delete_category(self, name):
        if name in self.categories:
            del self.categories[name]
            return True, "Category deleted successfully."
        return False, "Category does not exist."
    
    def add_expense(self, category, amount, notes):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if category not in self.categories:
            return False, "Category does not exist."
        self.categories[category]['expenses'].append({'amount': amount, 'notes': notes, 'timestamp': timestamp})
        return True, "Expense added successfully."
    
    def get_expenses(self):
        return self.expenses

    def save_data(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.categories, file)
        return "Data saved successfully."

    def load_data(self):
        try:
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def get_categories(self):
        return self.categories

    def get_expenses(self, category):
        if category in self.categories:
            return self.categories[category]['expenses']
        return []

    def get_category_names(self):
        return list(self.categories.keys())

    def get_pie_chart_data(self):
        labels = []
        sizes = []
        for category, data in self.categories.items():
            labels.append(category)
            total_expenses = sum(expense['amount'] for expense in data['expenses'])
            sizes.append(total_expenses)
        return labels, sizes
