document.getElementById("send-button").addEventListener("click", async () => {
    const title = document.getElementById("title").value;
    const news = document.getElementById("news").value;

    const statusMessageElement = document.getElementById("status-message");
    statusMessageElement.textContent = '';
    statusMessageElement.classList.remove('success', 'error');

    if (!title || !news) {
        statusMessageElement.textContent = "Please fill in all fields.";
        statusMessageElement.classList.add('error');
        return;
    }

    const data = {
        action: "UPDATE",
        data: { title, news }
    };

    try {
        const response = await fetch("http://localhost:8000/create-news/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            statusMessageElement.textContent = "News submitted successfully!";
            statusMessageElement.classList.add('success');
        } else {
            statusMessageElement.textContent = "Failed to submit news.";
            statusMessageElement.classList.add('error');
        }
    } catch (error) {
        console.error("Error:", error);
        statusMessageElement.textContent = "An error occurred while submitting news.";
        statusMessageElement.classList.add('error');
    }
});
const socket = new WebSocket("ws://localhost:8765/updates");

socket.onopen = () => {
    console.log("Connected to WebSocket server");
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    displayNewsUpdate(data);
};

function displayNewsUpdate(news) {
    console.log("Displaying news:", news);

    const newsListElement = document.getElementById("news-list");

    if (!newsListElement) {
        console.error("News list element not found.");
        return;
    }

    const newsItem = document.createElement("div");
    newsItem.classList.add("news-item");

    const titleElement = document.createElement("h3");
    titleElement.textContent = news.title;
    newsItem.appendChild(titleElement);

    const newsContent = document.createElement("p");
    newsContent.textContent = news.news;
    newsItem.appendChild(newsContent);
    newsListElement.prepend(newsItem);
    console.log("News added to list:", newsItem);
}
