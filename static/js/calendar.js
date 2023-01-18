document.addEventListener('DOMContentLoaded', function(){
    var today = new Date(),
        year = today.getFullYear(),
        month = today.getMonth(),
        monthTag =["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"],
        day = today.getDate(),
        days = document.getElementsByTagName('td'),
        selectedDay,
        setDate,
        daysLen = days.length;

    function Calendar(selector, options) {
        this.options = options;
        this.draw();
    }
    
    Calendar.prototype.draw  = function() {
        this.getOptions();
        this.drawDays();
        var that = this,
            pre = document.getElementsByClassName('pre-button'),
            next = document.getElementsByClassName('next-button');
            
            pre[0].addEventListener('click', function(){that.preMonth(); });
            next[0].addEventListener('click', function(){that.nextMonth(); });
        while(daysLen--) {
            days[daysLen].addEventListener('click', function(){that.clickDay(this); });
        }
    };
    
    Calendar.prototype.drawHeader = function(e) {
        var headDay = document.getElementsByClassName('head-day'),
            headMonth = document.getElementsByClassName('head-month');

            e?headDay[0].innerHTML = e : headDay[0].innerHTML = day;
            headMonth[0].innerHTML = monthTag[month] +" " + year;        
     };
    
    Calendar.prototype.drawDays = function() {
        let form = new FormData();

        form.append("requete", "mois");
        form.append("mois", month<9?"0"+(month+1):month+1);
        form.append("annee", year);
        let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let request = new Request("/ajax/calendar", {method: 'POST',
                                                      body: form,
                                                      headers: {"X-CSRFToken": csrfTokenValue}})
        fetch(request)
            .then(response => response.json())
            .then(result => {
                var vacations = [];
                var reunions = [];
                result.vacations.forEach(element => {
                    var temp_date = new Date(element.date_debut);
                    vacations.push(temp_date)
                });
                result.reunions.forEach(element => {
                    var temp_date = new Date(element.date);
                    reunions.push(temp_date)
                });


                var startDay = (new Date(year, month, 1).getDay()+6)%7,

                nDays = new Date(year, month + 1, 0).getDate(),
        
                n = startDay;

                for(var k = 0; k <42; k++) {
                    days[k].innerHTML = '';
                    days[k].id = '';
                    days[k].className = '';
                }

                console.log(vacations)
                for(var i  = 1; i <= nDays ; i++) {
                    days[n].innerHTML = i;
                    if((vacations.find(item => {return parseInt(item.getDate()) == i}) || []).length != 0){
                        days[n].classList.add("vacation")
                    }
                    if((reunions.find(item => {return parseInt(item.getDate()) == i}) || []).length != 0){
                        days[n].classList.add("reunion")
                    }
                    n++;
                }
                
                for(var j = 0; j < 42; j++) {
                    if(days[j].innerHTML === ""){
                        
                        days[j].id = "disabled";
                        
                    }else if(j === day + startDay - 1){
                        if((this.options && (month === setDate.getMonth()) && (year === setDate.getFullYear())) || (!this.options && (month === today.getMonth())&&(year===today.getFullYear()))){
                            this.drawHeader(day);
                            days[j].id = "today";
                        }
                    }
                    if(selectedDay){
                        if((j === selectedDay.getDate() + startDay - 1)&&(month === selectedDay.getMonth())&&(year === selectedDay.getFullYear())){
                        days[j].classList.add("selected");
                        this.drawHeader(selectedDay.getDate());
                        }
                    }
                }
            })
        
    };
    
    Calendar.prototype.clickDay = function(o) {
        var selected = document.getElementsByClassName("selected"),
            len = selected.length;
        if(len !== 0){
            selected[0].classList.remove("selected");
        }
        o.classList.add("selected");
        selectedDay = new Date(year, month, o.innerHTML);
        this.drawHeader(o.innerHTML);

        let form = new FormData();

        form.append("requete", "jour");
        form.append("jour", o.innerHTML);
        form.append("mois", month<9?"0"+(month+1):month+1);
        form.append("annee", year);
        let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let request = new Request("/ajax/calendar", {method: 'POST',
                                                      body: form,
                                                      headers: {"X-CSRFToken": csrfTokenValue}})
        fetch(request)
            .then(response => response.json())
            .then(result => {
                document.querySelector('#events').innerHTML = "";
                result.reunions.forEach(element => {
                    document.querySelector('#events').innerHTML += '<div class="card" style="width: 18rem;"><div class="card-body"><h5 class="card-title">'+element.membre.first_name+' '+element.membre.last_name+' et '+element.referent.first_name+' '+element.referent.last_name+'</h5><h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6></div></div>'
                });
                result.vacations.forEach(element => {
                    document.querySelector('#events').innerHTML += '<div class="card" style="width: 18rem;"><div class="card-body"><h5 class="card-title">'+element.nom+'</h5><h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6></div></div>'
                });
            });
        
    };
    
    Calendar.prototype.preMonth = function() {
        if(month < 1){ 
            month = 11;
            year = year - 1; 
        }else{
            month = month - 1;
        }
        this.drawHeader(1);
        this.drawDays();
    };
    
    Calendar.prototype.nextMonth = function() {
        if(month >= 11){
            month = 0;
            year =  year + 1; 
        }else{
            month = month + 1;
        }
        this.drawHeader(1);
        this.drawDays();
    };
    
    Calendar.prototype.getOptions = function() {
        if(this.options){
            var sets = this.options.split('-');
                setDate = new Date(sets[0], sets[1]-1, sets[2]);
                day = setDate.getDate();
                year = setDate.getFullYear();
                month = setDate.getMonth();
        }
    };
    
     Calendar.prototype.reset = function() {
         month = today.getMonth();
         year = today.getFullYear();
         day = today.getDate();
         this.options = undefined;
         this.drawDays();
     };
    
    Calendar.prototype.setCookie = function(name, expiredays){
        if(expiredays) {
            var date = new Date();
            date.setTime(date.getTime() + (expiredays*24*60*60*1000));
            var expires = "; expires=" +date.toGMTString();
        }else{
            var expires = "";
        }
        document.cookie = name + "=" + selectedDay + expires + "; path=/";
    };
    
    Calendar.prototype.getCookie = function(name) {
        if(document.cookie.length){
            var arrCookie  = document.cookie.split(';'),
                nameEQ = name + "=";
            for(var i = 0, cLen = arrCookie.length; i < cLen; i++) {
                var c = arrCookie[i];
                while (c.charAt(0)==' ') {
                    c = c.substring(1,c.length);
                    
                }
                if (c.indexOf(nameEQ) === 0) {
                    selectedDay =  new Date(c.substring(nameEQ.length, c.length));
                }
            }
        }
    };
    var calendar = new Calendar();
    
        
}, false);