class FlowControl{
	constructor(){
		this.flow = {
			element: null,
			flowId: null,
			isOn: false
		}
	}

	_createFlow(object, timeInterval=5){
		async function getAndUpdateStats(){
				const fetch_ = await object.getStats();
				object.updateStats(fetch_);
		}
		getAndUpdateStats();
		const reference = setInterval(getAndUpdateStats, timeInterval * 1000)
		return reference
	}

	stop(){
		clearInterval(this.flow.flowId);
		this.flow.isOn = false;
	}
	start(){
		this.flow = {
			flowId : this._createFlow(this.flow.element),
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
			flowId : this._createFlow(activeEl),
			element : activeEl,
			isOn : true
		}
	}
}



flowControl = new FlowControl();

const dashBoard = new DashBoard();
const disks = new Disks();

document.addEventListener("DOMContentLoaded",()=>{
	flowControl.changeFlow(dashBoard);
	document.querySelector('#home-tab').addEventListener("click", ()=>{flowControl.changeFlow(dashBoard)})
	document.querySelector('#hdds-tab') .addEventListener("click", ()=>{flowControl.changeFlow(disks)})
})

document.addEventListener("visibilitychange", ()=>{
	flowControl.toggle();
});
