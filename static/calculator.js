
const button = document.querySelector("#temple");
const div = document.querySelector("#class");
const store = document.querySelector("#store");
const detect = document.querySelector("#detect");
const templea = document.querySelector("#templea");

// for(deletes of deleteb){
// deletes.addEventListener('click',(ev)=>{
//     ev.preventDefault();
//     deleteb.parentElement.remove();
// })


button.addEventListener('click',(ev)=>{ //For Classes
        ev.preventDefault();
        const clone = div.cloneNode(true);
        div.querySelector("#delete").disabled = false;
        div.querySelector("#delete").addEventListener('click',(ev)=>{
            ev.preventDefault();
            div.querySelector("#delete").parentElement.remove();
        })
        clone.querySelector("#Classe").value = null;
        store.appendChild(clone);
        clone.querySelector("#delete").disabled = false;
        clone.querySelector("#delete").addEventListener('click',(ev)=>{
            ev.preventDefault();
            clone.querySelector("#delete").parentElement.remove();
        })
});

templea.addEventListener('click',(ev)=>{ //Activities
    ev.preventDefault();
    let div = document.querySelector("#active")
    const clone = div.cloneNode(true);
    div.querySelector("#deletea").disabled = false;
    div.querySelector("#deletea").addEventListener('click',(ev)=>{
        ev.preventDefault();
        div.querySelector("#deletea").parentElement.remove();
    })
    document.querySelector("#storea").appendChild(clone);
    clone.querySelector("#Teets").value = null;
    clone.querySelector("#deletea").disabled = false;
    clone.querySelector("#deletea").addEventListener('click',(ev)=>{
        ev.preventDefault();
        clone.querySelector("#deletea").parentElement.remove();
    })
});


detect.addEventListener('click',(ev)=>{
    ev.preventDefault();
    const selector = document.body.querySelectorAll("#vor");
    const selectora = document.body.querySelectorAll("#act");
    const cd = document.querySelectorAll("#class");
    const actives = document.querySelectorAll("#active");
    ev.preventDefault();
    stress = 0;
    for(need of selector){
        stress = stress + parseInt(need.value);
    }
    for(needa of selectora){
        stress = stress + parseInt(needa.value);
    }
    let classi = [];
    let activia = [];
    for(classe of cd){
        if(classe.querySelector("#Classe").value !== ""){
        let penop = { //''
            class: classe.querySelector("#Classe").value,
            difficultiy: classe.querySelector("#vor").options[classe.querySelector("#vor").selectedIndex].text
            };
            classi.push(penop);
        };
    }
    for(a of actives){
        if(a.querySelector("#Teets").value !== ""){
        let penop = {
            activity: a.querySelector("#Teets").value,
            category: a.querySelector("#act").options[a.querySelector("#act").selectedIndex].text
        };
        activia.push(penop);
    }
    }
    console.log(classi);
    console.log(activia);
    // Detect Intense Points
    let classes = "";
    let asctives = "";
    let suggestions = "";
    let activisuggestions = "";
    let counter = 0;
    let lecounter = 0;
    for(diff of classi){
        if(diff.difficultiy == "Hard"){
            if(counter <1){
                classes = diff.class
            }
            if(counter >=1){
                classes = classes + "," + diff.class;
            }
            counter = counter  + 1;
        }
    }

    for(activ of activia){
        if(activ.category === "Highly Engaging Club/Organization" || activ.category  === "High Frequency/Intensity Sport"){
            if(lecounter <1){
                asctives = activ.activity
            }
            if(lecounter >=1){
                asctives= asctives + "," + activ.activity;
            }
            lecounter = lecounter  + 1;
        }
    }


    if(counter <5 && counter>=3){
        suggestions = `You are taking numerous Hard Classes that include: ${classes}. This may increase the diffuclty to pass through this school year.`
    }
    else if(counter>=5){
         suggestions = `You are taking a significant amount of Hard Classes that include: ${classes}. You may want to have fewer activites or 
        the amount of hard classes you take.`
    }
    else{
        suggestions = `The Hard Classes you are taking are: ${classes}. You are not taking a significant amount of these classes and therefore should have a lighter school year.`
    }

    //Suggestionss
    console.log(lecounter);
    console.log(counter);
    if(lecounter <5 && lecounter>=3){
        activisuggestions = `You are taking a lot of highly engaging that include: ${asctives}. This may hinder performance in your classes due to the time filled up after school.`
    }
    else if(lecounter>=5){
        activisuggestions = `You are taking a significant amount of highly engaging activites that include: ${asctives}. You may want to reduce this amount and create a better balance between
        class and extracurricular activies for your school year.`
    }
    else{
        activisuggestions = `The only Highly Engaging Activies you are doing is: ${asctives}. You should not have a difficult time balancing school with these activities and they aren't a big factor to your school intensity.`
    }
    GenSug = ""
    if(lecounter >=5 && counter>=4){
        GenSug = "Overall Synposis: It seems that the amount of highly engaging extracurricular activies and hard classes you are taking this year likely will harm your overall performance in school." +
        " You will find it extremely difficulty to go through this school year and we suggest possible cutting down on certain classes/activities."
    }
    else if((lecounter <=5 && lecounter>=2) && (counter <=7 && counter>=2)){
        GenSug = "Overall Synposis: You are taking a high amount of hard classes and highly enaging extracurricular acitvities and this may dwindle your school performance. You may want to consider" 
        + " cutting down on certain acitvities/classes if you feel like this year may be too challenging. "
    }
    else if(lecounter >=3 && counter<2){ //Lots of activities but no classes
        GenSug = "Overall Synposis: You are taking a lot of highly intensive extracurricular activities but few hard classes. While this is fine, you may consider adding more classes to increase overall workload for this year or reducing the amount of activities during the year "
    }
    else if(lecounter <2 && counter>=3){ //More classes less activities
        GenSug = "Overall Synopsis: You are taking a lot of highly intensive classes with less activities. As a result, you may be too focused in academics without giving regard for activities, which may harm other aspects of learning. Consider taking fewer/less difficult classes so it may allow time for more extracurricular activities."
    }
    else{
        GenSug = "Overall Synposis: You do not have too many difficult hard classes and highly engaing extracurricular activities. As a result, you should be able to focus on" +
        " more on certain classes/activities and may consider even adding more load for this school year if you find it too easy. "
    }
    console.log(GenSug);

    let data = {
        classes: classi,
        activities: activia,
        ClassSuggestions: suggestions,
        ActvitySuggestions: activisuggestions,
        Synposis: GenSug
    }
   axios.post('/tag-user',{
    Intensity: check(stress),
    UserData: data
   }).then( function(response) {
     window.location = "/profile"

   })

})

function check(value){
    value = parseInt(value)
    if(value>=30){
        return "Extremely Intense School Year";
    }
    else if(30>value && value>=20){
        return "Very Intense School Year";
    }
    else if(20>value && value>=15){
        return "Intense School Year";
    }
    else if(15>value && value>=10){
        return "Somewhat Intense School Year";
    }
    else if(9>value){
        return "Not an Intense School Year";
    }
    else{
        return "invalid"
    }

}