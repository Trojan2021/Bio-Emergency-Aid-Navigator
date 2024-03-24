class ItemController{
    constructor(){
        this.bandaids = 0;
        this.gauzes = 0;
    }
    getBandaids(){
        return this.bandaids;
    }
    getGauze(){
        return this.gauzes;
    }
    incrementBandaids(){
        this.bandaids++;
    }
    decrementBandaids(){
        this.gauzes++;
    }
}
