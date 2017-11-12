public function findspeed(thing:GameObject):Number{
	var testv:Number; //Will be the random speed I return

	if (! cchanged){                          //Classical regime, use acceptance-rejectance
		var failed:Boolean = true;        //Keep track of good acceptance or rejectance
		var vmax:Number = 4*Math.sqrt(T); //A particle with speed v>vmax is very improbable, so impose this cutoff

		while (failed){
			testv = Math.random() * vmax;
                        /*Find probability distribution value of testv*/
                        var prob:Number = Math.sqrt(Math.E)*testv*Math.sqrt(thing.mass)/Math.sqrt(T)*Math.exp(-thing.mass*testv*testv/(2*T)));
			if (Math.random()<prob) failed = false; //This is a good value of the speed
			}
		}

	else{                                     //Relativistic regime
		var rat:Number = thing.mass/T;
		var p:Number = -Math.exp(-c*c*rat-1)*(Math.random()-1)*(1+c*c*rat); //Argument of Lambert W

		var L1:Number = Math.log(p);
		var L2:Number = Math.log(-L1);
		var lambertW:Number = L1-L2+L2/L1; //Assymptotic expansion of the Lambert W
		testv = -c*Math.sqrt( (1 + lambertW)*(1 + lambertW)-c*c*c*c*rat*rat )/(1+lambertW); //This is the inverse function of the cdf
		}

	return testv;
	}