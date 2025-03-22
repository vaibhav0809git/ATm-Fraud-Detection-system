document.getElementById('transactionForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const account_number = document.getElementById('account_number').value;
    const amount = document.getElementById('amount').value;
    const transaction_id = document.getElementById('transaction_id').value;

    fetch('http://127.0.0.1:5000/api/transactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            account_number: account_number,
            amount: amount,
            transaction_id: transaction_id
        }),
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        const successMessageDiv = document.getElementById('successMessage');

        // Clear previous messages
        resultDiv.innerHTML = '';
        successMessageDiv.classList.add('hidden');

        if (data.is_fraud) {
            resultDiv.innerHTML = '<p style="color: red;">Fraud Detected!</p>';
        } else {
            successMessageDiv.classList.remove('hidden'); // Show success message
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
