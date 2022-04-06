
class User {
    constructor(username, name, coach, cohort) {
        this.username = username;
        this.name = name;
        this.coach = coach;
        this.cohort = cohort;

        this.root = null;
        this.graphImageElement = null;
        this.profileImageElement = null;
        this.urlElement = null;
        this.labelElement = null;
        this.h1Element = null;
        this.h3Element = null;
    }

    asComponent(){
        if (this.root){
            while (this.root.firstChild) {
                this.root.removeChild(this.root.firstChild);
            }
        }
        this.createGraph();
        this.createProfile();
        this.createUrl();
        this.createH3();
        this.createLabel();

        this.root = document.createElement('div');
        this.root.appendChild(this.urlElement);
        this.root.appendChild(this.labelElement);
        this.root.appendChild(this.profileImageElement);
        this.root.appendChild(this.graphImageElement);


        getContribution(this.username).then(data => {
            this.graphImageElement.src = data.graph_image;
            this.graphImageElement.width = "1000";
            this.graphImageElement.height = "150";
            this.graphImageElement.style.display = "";
            this.profileImageElement.src = data.profile_image;
            this.profileImageElement.width = "150";
            this.profileImageElement.height = "150";
            this.profileImageElement.style.display = "";
            this.urlElement.href = data.url;
        })
        .catch(error => {
            console.error(error);
            this.graphImageElement.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/ProhibitionSign2.svg/1024px-ProhibitionSign2.svg.png"
            this.profileImageElement.src = "https://icon-library.com/images/unknown-person-icon/unknown-person-icon-4.jpg"
            this.profileImageElement.style.display = "";
            this.graphImageElement.style.display = "";
        })

        return this.root
    }

    createGraph(){
        this.graphImageElement = document.createElement("img");
        this.graphImageElement.className = "graph-image"
        this.graphImageElement.src = "https://media0.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif?cid=ecf05e47qgat0gh5s49q8ymszpqlmseyaqzi10leo077t1td&rid=giphy.gif&ct=g"
        this.graphImageElement.width = "50";
        this.graphImageElement.height = "50";
        this.graphImageElement.style.display = "none";
        this.graphImageElement.alt = `${this.username}_graph`
    }

    createProfile(){
        this.profileImageElement = document.createElement("img")
        this.profileImageElement.className = "profile-image"
        this.profileImageElement.src = "https://media0.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif?cid=ecf05e47qgat0gh5s49q8ymszpqlmseyaqzi10leo077t1td&rid=giphy.gif&ct=g"
        this.profileImageElement.width = "50";
        this.profileImageElement.height = "50";
        this.profileImageElement.style.display = "none";
        this.profileImageElement.alt = `${this.username}_profile`
    }

    createUrl(){
        this.urlElement = document.createElement("a");
        this.urlElement.href = `https://github.com/${this.username}`;
        this.urlElement.target = "_blank";

        this.h1Element = document.createElement("h1");
        this.h1Element.textContent = `${this.name} - ${this.cohort}`;
        this.h1Element.className = "user-header";

        this.urlElement.appendChild(this.h1Element);
    }

    createH3() {
        this.h3Element = document.createElement("h3");
        this.h3Element.textContent = `GitHub: ${this.username}`;
    }

    createLabel() {
        this.labelElement = document.createElement("h4");
        this.labelElement.textContent = `Coach: ${this.coach}`;
    }
}