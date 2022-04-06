function getTree() {
    // check that the version is correct
    let localTree = JSON.parse(localStorage.getItem('appacademycoaches') || '{}');
    return hasUpdates().then(updates => {
        if (updates || Object.keys(localTree).length == 0) {
            let localPss = localStorage.getItem('pss');
            return authenticate(localPss)
                .then(responseData => {
                    if (!responseData.error) {
                        localStorage.setItem('appacademycoaches', JSON.stringify(responseData));
                        return responseData;
                    }
                    return {};
                })
        }
        return localTree;
    });
}


function getStudents() {
    return getTree().then(data => data.students);
}