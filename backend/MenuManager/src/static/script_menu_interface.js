function loadRestaurantData() {
    const xhttp = new XMLHttpRequest();
    xhttp.open('GET', '/api/get_data', true);
    xhttp.onload = function () {
        if (xhttp.status === 200) {
            const data = JSON.parse(xhttp.responseText);
            const restaurantList = document.getElementById('restaurant-list');
            restaurantList.innerHTML = '';

            data.restaurants.forEach((restaurant, index) => {
                const button = document.createElement('button');
                button.textContent = restaurant.name;
                button.onclick = () => displayRestaurantData(data, index);
                restaurantList.appendChild(button);
            });
            
        } else {
            alert('Failed to fetch data');
        }
    };
    xhttp.send();
}

function displayRestaurantData(data, restaurantIndex) {
    const filtered_data = data.restaurants[restaurantIndex];
    
    const restaurantData = document.getElementById('restaurant-data');
    restaurantData.innerHTML = '';

    restaurantData.innerHTML = `
        <div class="restaurant">
            <h1>${filtered_data.name}</h1>
            ${filtered_data.menus.map(menu => `
                <h3>${menu.name}</h3>
                <div>
                    ${menu.categories.map(category => `
                        <h3>${category.name}</h3>
                        <ul>
                            ${category.items.map(item => `
                                <li class="menu-item">${item.name} - £${item.price}</li>
                                <ul>
                                    <li class="dietary-requirements">Dietary Requirements: ${item.dietary.length > 0 ? item.dietary.join(', ') : 'None'}</li>
                                    <li class="reward-eligible">Reward Eligible: ${item.rewardEligible ? 'Yes' : 'No'}</li>
                                </ul>
                            `).join('')}
                        </ul>
                    `).join('')}
                </div>
            `).join('')}
        </ul>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', loadRestaurantData);