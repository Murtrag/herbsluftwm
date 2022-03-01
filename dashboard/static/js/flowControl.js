function startFlow(object){
	const reference = setInterval(
	async ()=>{
			const fetch_ = await disks.getStats(["disks"])
			disks.updateDisks(fetch_.disks)
	}
	,5000)
	return reference
}

class FlowControl{
	constructor([...elements]){
		this.elements = elements;
	}

	stopAll(exception=null){
		// pass
		this.elements.foreach(el=>{
			if (el.name !== exception){
				el.stop()
			}else{
				el.start()
			}
		})
	}

	changeFlow(active){
		// pass
	}
}
