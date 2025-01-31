document.addEventListener('DOMContentLoaded', function() {
    const apiKey = 'Bearer L8hWquwn7hcSOGgYqu67KtDLxwqVTGlz';

    document.getElementById('addOrderBtn').addEventListener('click', function() {
        const userId = document.getElementById('userId').value;
        const itemsInput = document.getElementById('items').value;
        const items = itemsInput.split(',').map(item => {
            const [itemId, quantity] = item.split(':').map(str => str.trim());
            return { item_id: itemId, quantity: quantity || 1 };
        });

        fetch('/api/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': apiKey
            },
            body: JSON.stringify({ user_id: userId, items: items })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
        })
        .catch(error => console.error('Error adding order:', error));
    });

    document.getElementById('deleteOrderBtn').addEventListener('click', function() {
        const orderId = document.getElementById('deleteOrderId').value;

        fetch(`/api/orders/${orderId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': apiKey
            }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
        })
        .catch(error => console.error('Error deleting order:', error));
    });

    document.getElementById('deleteAllOrdersBtn').addEventListener('click', function() {
        fetch('/api/orders', {
            method: 'DELETE',
            headers: {
                'Authorization': apiKey
            }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
        })
        .catch(error => console.error('Error deleting all orders:', error));
    });

    document.getElementById('viewOrdersBtn').addEventListener('click', function() {
        fetch('/api/orders', {
            headers: {
                'Authorization': apiKey
            }
        })
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#ordersTable tbody');
            tableBody.innerHTML = '';
            data.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${order.order_id}</td>
                    <td>${order.user_id}</td>
                    <td>${order.order_date}</td>
                    <td>${order.status}</td>
                    <td>${order.items.map(item => `${item.item_id} (x${item.quantity})`).join(', ')}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching orders:', error));
    });
});