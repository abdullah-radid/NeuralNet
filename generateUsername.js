function generateRandomUsername() {
    const randomNumber = Math.floor(10000 + Math.random() * 90000); 
    return `User${randomNumber}`; // user + random 5-digit number
}

module.exports = generateRandomUsername;
