class FlowControl{
	constructor(){
		this.serverError = new ServerError();
		this.flow = {
			element: null,
			intervalId: null,
			isOn: false
		}
	}

	_createFlow(object, timeInterval=5){
		const getAndUpdateStats = async ()=>{
				try{
					const fetch_ = await object.getStats();
					if (fetch_.isAfk === false){
						object.updateStats(fetch_);
						this.serverError.hide()
				}
				}catch(err){
						this.serverError.show();
						this.serverError.addTitleMessage(err);
				}
		}
		getAndUpdateStats();
		const reference = setInterval(getAndUpdateStats, timeInterval * 1000)
		return reference
	}

	stop(){
		clearInterval(this.flow.intervalId);
		this.flow.isOn = false;
	}
	start(){
		this.stop();
		this.flow = {
			// ...this.flow,
			element: this.flow.element,
			intervalId : this._createFlow(this.flow.element),
			isOn : false
		}
	}
	toggle(){
		if(this.flow.isOn){
			this.stop()
		}else{
			this.start()
		}
	}

	changeFlow(activeEl){
		this.stop();
		this.flow = {
			intervalId : this._createFlow(activeEl),
			element : activeEl,
			isOn : true
		}
	}
}



const flowControl = new FlowControl();

const dashBoard = new DashBoard();
const disks = new Disks();

// nav tab activity
document.addEventListener("DOMContentLoaded",()=>{
	flowControl.changeFlow(dashBoard);
	document.querySelector('#home-tab').addEventListener("click", ()=>{flowControl.changeFlow(dashBoard)})
	document.querySelector('#hdds-tab') .addEventListener("click", ()=>{flowControl.changeFlow(disks)})
})


// Webbroser activity
document.addEventListener("visibilitychange", ()=>{
	flowControl.toggle();
});
window.addEventListener('blur', ()=>{
	flowControl.stop();
});
window.addEventListener('focus', ()=>{
	flowControl.start();
});
