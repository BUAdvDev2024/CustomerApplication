function fetchData() {
    const xhttp = new XMLHttpRequest();
    xhttp.open('GET', '/api/get_data', true);
    xhttp.onload = function () {
        if (xhttp.status === 200) {
            const data = JSON.parse(xhttp.responseText);
            renderData(data);
        } else {
            alert('Failed to fetch data');
        }
    };
    xhttp.send();
}

function renderData(data) {
    const container = document.getElementById('restaurants-container');
    container.innerHTML = '';

    data.restaurants.map((restaurant, restaurantIndex) => {
        const restaurantCard = document.createElement('div');
        restaurantCard.className = 'restaurant-card';
        restaurantCard.innerHTML = `
            <div class="restaurant">
                <label for="restaurant-${restaurantIndex}">Restaurant:</label>
                <input type="text" value="${restaurant.name}" id="restaurant-${restaurantIndex}">
                <button onclick="updateRestaurant(${restaurantIndex})">Update Restaurant Name</button>
                <button onclick="deleteRestaurant(${restaurantIndex})">Delete Restaurant</button>
                ${restaurant.menus.map((menu, menuIndex) => `
                    <div class="menu">
                        <label for="menu-${restaurantIndex}-${menuIndex}">Menu:</label>
                        <input type="text" value="${menu.name}" id="menu-${restaurantIndex}-${menuIndex}">
                        <button onclick="updateMenu(${restaurantIndex}, ${menuIndex})">Update Menu Name</button>
                        <button onclick="deleteMenu(${restaurantIndex}, ${menuIndex})">Delete Menu</button>
                        ${menu.categories.map((category, categoryIndex) => `
                            <div class="category">
                                <label for="category-${restaurantIndex}-${menuIndex}-${categoryIndex}">Category:</label> 
                                <input type="text" value="${category.name}" id="category-${restaurantIndex}-${menuIndex}-${categoryIndex}">
                                <button onclick="updateCategory(${restaurantIndex}, ${menuIndex}, ${categoryIndex})">Update Category</button>
                                <button onclick="deleteCategory(${restaurantIndex}, ${menuIndex}, ${categoryIndex})">Delete Category</button>
                                ${category.items.map((item, itemIndex) => `
                                    <div class="item">
                                        <label for="item-name-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}">Item:</label>
                                        <input type="text" value="${item.name}" id="item-name-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}">
                                        <label for="item-price-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}">Price: £</label>
                                        <input type="number" step="0.01" value="${item.price}" placeholder="0.00" min="0.00" id="item-price-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}">
                                        ${item.dietary.map((dietary, dietaryIndex) => `
                                            <div class="dietary">
                                                <label for="item-dietary-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}-${dietaryIndex}">Dietary/Allergy Info:</label>
                                                <input type="text" value="${dietary}" id="item-dietary-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}-${dietaryIndex}">
                                                <button onclick="updateDietaryRequirement(${restaurantIndex}, ${menuIndex}, ${categoryIndex}, ${itemIndex}, ${dietaryIndex})">Update Dietary Requirement</button>
                                                <button onclick="deleteDietaryRequirement(${restaurantIndex}, ${menuIndex}, ${categoryIndex}, ${itemIndex}, ${dietaryIndex})">Delete Dietary Requirement</button>
                                            </div>
                                        `).join('')}
                                        <button onclick="addDietaryRequirement(${restaurantIndex}, ${menuIndex}, ${categoryIndex}, ${itemIndex})">Add Dietary Requirement</button>
                                        <label for="item-reward-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}">Reward Eligible:</label>
                                        <input type="checkbox" id="item-reward-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}">
                                        <button onclick="updateItem(${restaurantIndex}, ${menuIndex}, ${categoryIndex}, ${itemIndex})">Update Item Details</button>
                                        <button onclick="deleteItem(${restaurantIndex}, ${menuIndex}, ${categoryIndex}, ${itemIndex})">Delete Item</button>
                                    </div>
                                `).join('')}
                                <button onclick="addItem(${restaurantIndex}, ${menuIndex}, ${categoryIndex})">Add Item</button>
                            </div>
                        `).join('')}
                        <button onclick="addCategory(${restaurantIndex}, ${menuIndex})">Add Category</button>
                    </div>
                `).join('')}
                <button onclick="addMenu(${restaurantIndex})">Add Menu</button>
            </div>
        `;
        container.appendChild(restaurantCard);
    });
    const addRestaurantButton = document.createElement('button');
    addRestaurantButton.textContent = 'Add Restaurant';
    addRestaurantButton.onclick = addRestaurant;
    container.appendChild(addRestaurantButton);
}

function updateRestaurant(restaurantIndex) {
    let name = document.getElementById(`restaurant-${restaurantIndex}`).value;
    const path = ['restaurants', restaurantIndex, 'name'];
    const newData = name ;
    const xhttp = new XMLHttpRequest();
    xhttp.open('PUT', '/api/update_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to update restaurant');
    };
    xhttp.send(JSON.stringify({ path, newData }));
}

function updateMenu(restaurantIndex, menuIndex) {
    let name = document.getElementById(`menu-${restaurantIndex}-${menuIndex}`).value;
    const path = ['restaurants', restaurantIndex, 'menus', menuIndex, 'name'];
    const newData = name;
    const xhttp = new XMLHttpRequest();
    xhttp.open('PUT', '/api/update_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to update menu');
    };
    xhttp.send(JSON.stringify({ path, newData }));
}

function updateCategory(restaurantIndex, menuIndex, categoryIndex) {
    let name = document.getElementById(`category-${restaurantIndex}-${menuIndex}-${categoryIndex}`).value;
    const path = ['restaurants', restaurantIndex, 'menus', menuIndex, 'categories', categoryIndex, 'name'];
    const newData = name;
    const xhttp = new XMLHttpRequest();
    xhttp.open('PUT', '/api/update_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to update category');
    };
    xhttp.send(JSON.stringify({ path, newData }));
}

function updateItem(restaurantIndex, menuIndex, categoryIndex, itemIndex) {
    let name = document.getElementById(`item-name-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}`).value;
    let price = document.getElementById(`item-price-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}`).value;
    let rewardEligible = document.getElementById(`item-reward-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}`).checked;
    const path = ['restaurants', restaurantIndex, 'menus', menuIndex, 'categories', categoryIndex, 'items', itemIndex];
    price = parseFloat(price);
    const newData = { name, price, rewardEligible };
    const xhttp = new XMLHttpRequest();
    xhttp.open('PUT', '/api/update_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to update item');
    };
    xhttp.send(JSON.stringify({ path, newData }));
}

function updateDietaryRequirement(restaurantIndex, menuIndex, categoryIndex, itemIndex, dietaryIndex) {
    let dietary = document.getElementById(`item-dietary-${restaurantIndex}-${menuIndex}-${categoryIndex}-${itemIndex}-${dietaryIndex}`).value;
    const path = ['restaurants', restaurantIndex, 'menus', menuIndex, 'categories', categoryIndex, 'items', itemIndex, 'dietary', dietaryIndex];
    const newData = dietary;
    const xhttp = new XMLHttpRequest();
    xhttp.open('PUT', '/api/update_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to update dietary requirement');
    };
    xhttp.send(JSON.stringify({ path, newData }));
}

function addRestaurant() {
    let newData = { name: '', menus: [ { name: '', categories: [{ name: '', items: [{name: '', price: 0.00, dietary: [], rewardEligible: false }] }]}] };
    const path = ['restaurants'];
    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/add_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to add restaurant');
    };
    xhttp.send(JSON.stringify({ path, newData }));
}

function addMenu(restaurantIndex) {
    let newData = { name: '', categories: [{ name: '', items: [{name: '', price: 0.00, dietary: [], rewardEligible: false }] }] };
    const path = ['restaurants', restaurantIndex, 'menus'];
    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/add_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to add menu');
    };
    xhttp.send(JSON.stringify({ path, newData }));
}

function addCategory(restaurantIndex, menuIndex) {
    let newData = { name: '', items: [{name: '', price: 0.00, dietary: [], rewardEligible: false }] };
    const path = ['restaurants', restaurantIndex, 'menus', menuIndex, 'categories'];
    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/add_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to add category');
    };
    xhttp.send(JSON.stringify({ path, newData }));
}

function addItem(restaurantIndex, menuIndex, categoryIndex) {
    let newData = { name: '', price: 0.00, dietary: [], rewardEligible: false };
    const path = ['restaurants', restaurantIndex, 'menus', menuIndex, 'categories', categoryIndex, 'items'];
    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/add_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to add category');
    };
    xhttp.send(JSON.stringify({ path, newData }));
}

function addDietaryRequirement(restaurantIndex, menuIndex, categoryIndex, itemIndex) {
    let newData = '';
    const path = ['restaurants', restaurantIndex, 'menus', menuIndex, 'categories', categoryIndex, 'items', itemIndex, 'dietary'];
    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/add_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to add dietary requirement');
    };
    xhttp.send(JSON.stringify({ path, newData }));
}

function deleteRestaurant(restaurantIndex) {
    const path = ['restaurants', restaurantIndex];
    const xhttp = new XMLHttpRequest();
    xhttp.open('DELETE', '/api/delete_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to delete restaurant');
    };
    xhttp.send(JSON.stringify({ path }));
}

function deleteMenu(restaurantIndex, menuIndex) {
    const path = ['restaurants', restaurantIndex, 'menus', menuIndex];
    const xhttp = new XMLHttpRequest();
    xhttp.open('DELETE', '/api/delete_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to delete menu');
    };
    xhttp.send(JSON.stringify({ path }));
}

function deleteCategory(restaurantIndex, menuIndex, categoryIndex) {
    const path = ['restaurants', restaurantIndex, 'menus', menuIndex, 'categories', categoryIndex];
    const xhttp = new XMLHttpRequest();
    xhttp.open('DELETE', '/api/delete_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to delete category');
    };
    xhttp.send(JSON.stringify({ path }));
}

function deleteItem(restaurantIndex, menuIndex, categoryIndex, itemIndex) {
    const path = ['restaurants', restaurantIndex, 'menus', menuIndex, 'categories', categoryIndex, 'items', itemIndex];
    const xhttp = new XMLHttpRequest();
    xhttp.open('DELETE', '/api/delete_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to delete item');
    };
    xhttp.send(JSON.stringify({ path }));
}

function deleteDietaryRequirement(restaurantIndex, menuIndex, categoryIndex, itemIndex, dietaryIndex) {
    const path = ['restaurants', restaurantIndex, 'menus', menuIndex, 'categories', categoryIndex, 'items', itemIndex, 'dietary', dietaryIndex];
    const xhttp = new XMLHttpRequest();
    xhttp.open('DELETE', '/api/delete_data', true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.onload = function () {
        if (xhttp.status === 200) fetchData();
        else alert('Failed to delete dietary requirement');
    };
    xhttp.send(JSON.stringify({ path }));
}

document.addEventListener('input', function(event) {
    const input = event.target;

    // This is here to sort of fix the issue where the value 0 is not displayed as 0.00
    if (input.tagName === 'INPUT' && input.type === 'number') {
        input.value = parseFloat(input.value).toFixed(2);
    }

    if (input.tagName === 'INPUT' && (input.type === 'text' || input.type === 'number'|| input.type === 'checkbox')) {
        if (!input.hasAttribute('original-value')) {
            if (input.type === 'checkbox') {
                input.setAttribute('original-value', false);
            } else {
                input.setAttribute('original-value', input.defaultValue);
            }
        }

        var originalValue = input.getAttribute('original-value');
        var currentValue
        if (input.type === 'checkbox') {
            originalValue = input.getAttribute('original-value');
            currentValue = input.checked;
        } else if (input.type === 'text' || input.type === 'number') {
            originalValue = input.getAttribute('original-value');
            currentValue = input.value;
        }
        
        if (originalValue !== currentValue.toString()) {
            console.log('Input changed from original value:', originalValue, 'to:', currentValue);
            if (input.type === 'checkbox') {
                checkBoxLable = input.parentElement.querySelector(`label[for="${input.id}"]`);
                checkBoxLable.style.backgroundColor = 'yellow';
            } else{
                input.style.backgroundColor = 'yellow';
            }
        } else {
            console.log('Input value is the same as original value:', originalValue);
            if (input.type === 'checkbox') {
                checkBoxLable = input.parentElement.querySelector(`label[for="${input.id}"]`);
                checkBoxLable.style.backgroundColor = 'white';
            } else{
                input.style.backgroundColor = 'white';
            }
        }
    }
});

document.addEventListener('DOMContentLoaded', fetchData);