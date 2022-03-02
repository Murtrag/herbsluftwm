class DashBoard {
    constructor() {
        this.batteryCap = document.querySelector('#batteryCap');
        this.batteryPrediction = document.querySelector('#batteryPrediction');
        this.load = document.querySelector('#load');
        this.memory = document.querySelector('#memoryUsage');
        this.memoryPercentage = document.querySelector('#memoryPercentage');

		this.requiredStats = ["battery", "load", "memory", "batteryPrediction"]
    }

    async fetch(endpoint, [...query]){
        const resp = await fetch(`/${endpoint}`, {
            method: 'POST', // or 'PUT'
            headers: { 'Content-Type': 'application/json', },
            body: JSON.stringify({'query': query})
        })
        const promise = await resp.json();
        return promise
    }
getStats(stats=this.requiredStats) {
        // e.g. obj.getStats(["battery", "memory"])
        return this.fetch('stats', stats);
    }
    updateBatteryPrediction(value){
        this.batteryPrediction .innerHTML = value;
    }

    updateMemory({used_memory, total_memory, percentage_memory}){
        this.memory.innerHTML = `${used_memory} / ${total_memory}` ;
        this.memoryPercentage.innerHTML = `(${percentage_memory})`
    }

    updateLoad(value){
        this.load.innerHTML = value.join(' / ');
        }

    updateBattery(value){
        this.batteryCap.innerHTML = `${value}/100`;
    }


    updateStats({batteryPrediction, memory, battery, load}){
        this.updateLoad(load);
        this.updateMemory(memory);
        this.updateBattery(battery);
        this.updateBatteryPrediction(batteryPrediction);

    }
}
class ControlProporties{
    constructor(){
        this.screenBrightness = document.querySelector('#screenBrightness')
    }
}

window.addEventListener('DOMContentLoaded', (event) => {


    screenBrightness.addEventListener('change', (el)=>{
        // console.log(el.target.value)
        fetch('/brightness', {
            method: 'PUT', 
            headers: { 'Content-Type': 'application/json', },
            body: JSON.stringify({'brightness': el.target.value})
        })
            .then(response => response.json())
            .then(data => console.log(data));
    })

    audioVolume .addEventListener('change', (el)=>{
        // console.log(el.target.value)
        fetch('/audio', {
            method: 'PUT', 
            headers: { 'Content-Type': 'application/json', },
            body: JSON.stringify({'audio': el.target.value})
        })
            .then(response => response.json())
            .then(data => console.log(data));
    })
});
