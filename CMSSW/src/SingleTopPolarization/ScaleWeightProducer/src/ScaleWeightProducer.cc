// -*- C++ -*-
//
// Package:    ScaleWeightProducer
// Class:      ScaleWeightProducer
// 
/**\class ScaleWeightProducer ScaleWeightProducer.cc SingleTopPolarization/ScaleWeightProducer/src/ScaleWeightProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Andres Tiko
//         Created:  R märts  6 11:12:05 EET 2015
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


//
// class declaration
//

class ScaleWeightProducer : public edm::EDProducer {
   public:
      explicit ScaleWeightProducer(const edm::ParameterSet&);
      ~ScaleWeightProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
ScaleWeightProducer::ScaleWeightProducer(const edm::ParameterSet& iConfig)
{
   //register your products
/* Examples
   produces<ExampleData2>();

   //if do put with a label
   produces<ExampleData2>("label");
 
   //if you want to put into the Run
   produces<ExampleData2,InRun>();
*/
   //now do what ever other initialization is needed
  
}


ScaleWeightProducer::~ScaleWeightProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
ScaleWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
    using namespace std;

    /*edm::Handle<GenEventInfoProduct> genInfo;
    evt_info->weight()*wgt.wgt/lhe_info->originalXWGTUP()   
    // const LHEEventProduct::WGT& wgt = lhe_info->weights().at(iwgt);
    iEvent.getByLabel("generator", genInfo); 
    const GenEventInfoProduct& genEventInfo = *(genInfo.product());
    double Q_scale = genEventInfo.qScale();
    */
}

// ------------ method called once each job just before starting event loop  ------------
void 
ScaleWeightProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
ScaleWeightProducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
ScaleWeightProducer::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
ScaleWeightProducer::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
ScaleWeightProducer::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
ScaleWeightProducer::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
ScaleWeightProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(ScaleWeightProducer);
