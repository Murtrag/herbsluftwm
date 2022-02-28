class Badge{
	constructor(path, label, size, temp){
		// div
		this.badge = document.createElement("div");
		this.badge.classList = "col-4 text-center";

		//button
		this.button = document.createElement("button");
		this.button.classList = "btn btn-outline-success";
		// this.name = name;
		this.name = document.createElement('span');
		this.name.classList = "disk_name"
		this.name.innerText = `${path} ( ${label} )` 

		// this.size = size;
		this.size = document.createElement('span');
		this.size.classList = "disk_cappacity"
		this.size.innerText = `Cappacity: ${size}` 
		// this.temp = temp;
		this.temp = document.createElement('span');
		this.temp.classList = "disk_temperature"
		this.temp.innerText = `Temperature: ${temp}°C`;

	}
	getBadge(){
		this.button.append(
			this.name,
			this.size,
			this.temp
			)
		this.badge.appendChild(this.button)
		return this.badge
	}
	
}
const BadgeFactory = {
	create: function (path, label, size, temp){
		return (new Badge(path, label, size, temp)).getBadge()
	}
}


class Disks {
	constructor() {
		this.diskContainer = document.querySelector('#hdds .row');
	}
    async fetch(endpoint, [...query]){ //@TODO all fetch api functionality should be exported to separated class
        const resp = await fetch(`/${endpoint}`, {
            method: 'POST', // or 'PUT'
            headers: { 'Content-Type': 'application/json', },
            body: JSON.stringify({'query': query})
        })
        const promise = await resp.json();
        return promise
    }
    getStats([...stats]) {
		// console.log(stats)
        return this.fetch('stats', stats);
    }
	updateDisks(diskList){
		this.diskContainer.innerHTML = ""
		const badges = diskList.map(e=> BadgeFactory.create(e.path, e.label, e.size, e.temp))
		this.diskContainer.append(...badges)
	}

}

let disks = new Disks();

const updateDisks = setInterval(
async ()=>{
		const fetch_ = await disks.getStats(["disks"])
		disks.updateDisks(fetch_.disks)
}
,5000)
