let controller = new AbortController();

function addOption(component, value){
    let option = document.createElement("option");
    option.value = value;
    option.text = value;
    component.appendChild(option)
}


function searchContributions(e){
    clearUserComponents();
    controller.abort();
    controller = new AbortController();
    getTree().then(tree => {
        if (tree && tree.students && Object.entries(tree).length) {
            let rootElement = document.getElementById("root");
            let div = document.createElement("div");
            div.className = "user-container";
            rootElement.appendChild(div);

            let coach = document.getElementById('coach');
            let cohort = document.getElementById('cohort');
            let coach_text = coach.options[coach.selectedIndex].text;
            let cohort_text = cohort.options[cohort.selectedIndex].text;

            let results = tree.root[coach_text][cohort_text];
            let students = tree.students;
            Object.entries(results).forEach(pair => {
                let [name, username] = pair;
                let student = students[username];
                const user = new User(username, name, student.coach, student.cohort);
                div.appendChild(user.asComponent());
            })
        }
    });
}


function reloadTree(){
    getTree().then(tree => {
        let coach = document.getElementById('coach')
        let cohort = document.getElementById('cohort')
        while (cohort.firstChild)
            cohort.removeChild(cohort.firstChild);
        while (coach.firstChild)
            coach.removeChild(coach.firstChild);
        if (tree && Object.entries(tree).length) {
            addOption(coach, 'all');
            Object.keys(tree.root).forEach(c => {if (c !== 'all') addOption(coach, c)});
            addOption(cohort, "all");
            Object.keys(tree.root['all']).forEach(c => {if (c !== 'all') addOption(cohort, c)});
            coach.options.selectedIndex = 0;
        }
    });
}


function onCoachChange(){
    document.getElementById("coach").addEventListener('change', e => {
        getTree().then(tree => {
            if (tree && Object.entries(tree.root).length) {
                let coach = e.target.options[e.target.selectedIndex].text;
                let cohort = document.getElementById('cohort')
                while (cohort.firstChild) {
                    cohort.removeChild(cohort.firstChild)
                }
                addOption(cohort, "all");
                Object.keys(tree.root[coach]).forEach(c => {
                    if (c !== 'all')
                        addOption(cohort, c);
                })
            }
        })
    })
}


window.addEventListener('DOMContentLoaded', e=>{
    reloadTree();
    onCoachChange();
})


window.navbar = {
    reloadTree
}