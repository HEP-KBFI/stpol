// -*- C++ -*-
//
// Package:    LHEWeightProducer
// Class:      LHEWeightProducer
// 
/**\

 Description: Extracts the LHE weights from the LHEInfo structure and puts it into the event as simple doubles

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  ANdres Tiko
//         Created:  Mon Jun 8 21:13:42 EET 2013
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include <SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h>
#include <SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h>

#include <TMath.h>

class LHEWeightProducer : public edm::EDProducer {
   public:
      explicit LHEWeightProducer(const edm::ParameterSet&);
      ~LHEWeightProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      const edm::InputTag theSrc;
      const edm::InputTag genSrc;
};

LHEWeightProducer::LHEWeightProducer(const edm::ParameterSet& iConfig)
: theSrc(edm::InputTag("source"))
, genSrc(edm::InputTag("generator"))
{
   produces<double>("lheweight");
   produces<double>("lheweightup");
   produces<double>("lheweightdown");  
}


LHEWeightProducer::~LHEWeightProducer()
{
}

// ------------ method called to produce the data  ------------
void
LHEWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    edm::Handle<LHEEventProduct> EvtHandle ;
    iEvent.getByLabel( theSrc , EvtHandle ) ;    
    edm::Handle<GenEventInfoProduct> genEventInfo;
    iEvent.getByLabel(genSrc, genEventInfo);

    double gen_w = TMath::QuietNaN();
        
    if (genEventInfo.isValid())
        gen_w = genEventInfo->weight();
   
    double w = TMath::QuietNaN();
    double w_up = TMath::QuietNaN();
    double w_down = TMath::QuietNaN();

    const LHEEventProduct::WGT& wgt_nom = EvtHandle->weights().at(0);
    const LHEEventProduct::WGT& wgt_up = EvtHandle->weights().at(4);
    const LHEEventProduct::WGT& wgt_down = EvtHandle->weights().at(8);
    //std::cout << gen_w << std::endl;
    if (gen_w > 0)
        gen_w = 1;
    else
        gen_w = -1;
    w = gen_w*wgt_nom.wgt/EvtHandle->originalXWGTUP();
    w_up = gen_w*wgt_up.wgt/EvtHandle->originalXWGTUP();
    w_down = gen_w*wgt_down.wgt/EvtHandle->originalXWGTUP();
    
    std::auto_ptr<double> pOut(new double(w));
    iEvent.put(pOut, "lheweight");
    std::auto_ptr<double> pOut_up(new double(w_up));
    iEvent.put(pOut_up, "lheweightup");
    std::auto_ptr<double> pOut_down(new double(w_down));
    iEvent.put(pOut_down, "lheweightdown");
}

// ------------ method called once each job just before starting event loop  ------------
void 
LHEWeightProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
LHEWeightProducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
LHEWeightProducer::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
LHEWeightProducer::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
LHEWeightProducer::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
LHEWeightProducer::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
LHEWeightProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(LHEWeightProducer);
