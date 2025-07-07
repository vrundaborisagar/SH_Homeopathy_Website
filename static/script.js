function processOrder() {
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const number = document.getElementById('number').value;
    const kit = document.getElementById('kit').value;
    const paymentMethod = document.getElementById('paymentMethod').value;
    const price = 2550;

    // Here you would typically send the order details to your server
    // For demonstration, we'll just log it to the console
    console.log(`Order Details:
        Name: ${name}
        Address: ${address}
        Phone Number: ${number}
        Kit: ${kit}
        Payment Method: ${paymentMethod}
        Price: ${price} Rs.`);

    // Simulate opening the payment app (this is a mockup)
    alert(`Opening ${paymentMethod} for payment of ${price} Rs.`);

    // Here you would handle sending confirmation emails and SMS
    // This requires server-side code and a service to send emails/SMS
}
