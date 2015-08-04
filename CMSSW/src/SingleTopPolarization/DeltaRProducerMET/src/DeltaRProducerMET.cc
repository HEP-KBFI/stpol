// -*- C++ -*-
//
// Package:    DeltaRProducerMET
// Class:      DeltaRProducerMET
// 
/**\class DeltaRProducerMET DeltaRProducerMET.cc SingleTopPolarization/DeltaRProducerMET/src/DeltaRProducerMET.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Andres Tiko
//         Created:  E mai  25 17:12:49 EET 2015
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

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include <DataFormats/PatCandidates/interface/Muon.h>
#include <DataFormats/PatCandidates/interface/Electron.h>
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include <TMath.h>
#include <Math/GenVector/VectorUtil.h>

//
// class declaration
//

class DeltaRProducerMET : public edm::EDProducer {
   public:
      explicit DeltaRProducerMET(const edm::ParameterSet&);
      ~DeltaRProducerMET();

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
      const edm::InputTag muonSrc;
      const edm::InputTag electronSrc;
      //const edm::InputTag jetSrc;
      const edm::InputTag metSrc;
      
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
DeltaRProducerMET::DeltaRProducerMET(const edm::ParameterSet& iConfig)
: muonSrc(iConfig.getParameter<edm::InputTag>("muonSrc"))
, electronSrc(iConfig.getParameter<edm::InputTag>("electronSrc"))
, metSrc(iConfig.getParameter<edm::InputTag>("metSrc"))
{
   //produces<std::vector<pat::Jet> >("jets").setBranchAlias("jets");
   produces<std::vector<pat::Muon> >("muons").setBranchAlias("muons");
   produces<std::vector<pat::Electron> >("electrons").setBranchAlias("electrons");
   //now do what ever other initialization is needed
  
}


DeltaRProducerMET::~DeltaRProducerMET()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
DeltaRProducerMET::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   
   Handle<View<reco::Candidate> > muons;
   Handle<View<reco::Candidate> > electrons;
   Handle<std::vector<pat::MET> > mets;
   //Handle<View<reco::Candidate> > jets;
   
   iEvent.getByLabel(muonSrc, muons);   
   iEvent.getByLabel(electronSrc, electrons);   
   //iEvent.getByLabel(jetSrc, jets);   
   iEvent.getByLabel(metSrc, mets);

   //std::auto_ptr<std::vector<pat::Jet> > outJets(new std::vector<pat::Jet>());
   std::auto_ptr<std::vector<pat::Muon> > outMuons(new std::vector<pat::Muon>());
   std::auto_ptr<std::vector<pat::Electron> > outElectrons(new std::vector<pat::Electron>());
   
   if(mets->size() > 0){
       const pat::MET& met = mets->at(0);
       
        for ( uint i = 0; i < muons->size(); ++i ) {
            const pat::Muon& muon = (pat::Muon &)muons->at(i);
            float deltaR, deltaPhi;
            deltaR = ROOT::Math::VectorUtil::DeltaR(muon.p4(), met.p4());
            deltaPhi = ROOT::Math::VectorUtil::DeltaPhi(muon.p4(), met.p4());
            
            outMuons->push_back(muon);
            pat::Muon& mymuon = outMuons->back();
            mymuon.addUserFloat("deltaRMET", deltaR); 
            mymuon.addUserFloat("deltaPhiMET", deltaPhi); 
            //std::cout << "DeltaRMET: " << deltaR << std::endl;        
        }
        for ( uint i = 0; i < electrons->size(); ++i ) {
            const pat::Electron& electron = (pat::Electron &)electrons->at(i);
            float deltaR, deltaPhi;
            deltaR = ROOT::Math::VectorUtil::DeltaR(electron.p4(), met.p4());
            deltaPhi = ROOT::Math::VectorUtil::DeltaPhi(electron.p4(), met.p4());
            outElectrons->push_back(electron);
            pat::Electron& myelectron = outElectrons->back();
            
            myelectron.addUserFloat("deltaRMET", deltaR); 
            myelectron.addUserFloat("deltaPhiMET", deltaPhi); 
            //std::cout << "DeltaRMET: " << deltaR << std::endl;        
        }
   }

   
   iEvent.put(outMuons, "muons");
   iEvent.put(outElectrons, "electrons");
   //iEvent.put(outJets, "jets");
}

// ------------ method called once each job just before starting event loop  ------------
void 
DeltaRProducerMET::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
DeltaRProducerMET::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
DeltaRProducerMET::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
DeltaRProducerMET::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
DeltaRProducerMET::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
DeltaRProducerMET::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
DeltaRProducerMET::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(DeltaRProducerMET);
