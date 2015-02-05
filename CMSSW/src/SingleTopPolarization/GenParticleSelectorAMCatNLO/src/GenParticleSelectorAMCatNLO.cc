// -*- C++ -*-
//
// Package:    GenParticleSelectorAMCatNLO
// Class:      GenParticleSelectorAMCatNLO
//
/**\class GenParticleSelectorAMCatNLO GenParticleSelectorAMCatNLO.cc SingleTopPolarization/GenParticleSelectorAMCatNLO/src/GenParticleSelectorAMCatNLO.cc
 
 Description: [one line class summary]
 
 Implementation:
 [Notes on implementation]
 */
//
// Original Author:  Andres Tiko
//         Created:  R jan    30 11:47:22 EEST 2015
// $Id$
//
//


// system include files
#include <memory>
#include <TMath.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

using namespace edm;
using namespace std;
using namespace reco;

//
// class declaration
//

class GenParticleSelectorAMCatNLO : public edm::EDProducer {
public:
    explicit GenParticleSelectorAMCatNLO(const edm::ParameterSet&);
    ~GenParticleSelectorAMCatNLO();
    
    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
    
private:
    edm::InputTag _srcTag;

    virtual void beginJob() ;
    virtual void produce(edm::Event&, const edm::EventSetup&);
    virtual void endJob() ;
    
    virtual void beginRun(edm::Run&, edm::EventSetup const&);
    virtual void endRun(edm::Run&, edm::EventSetup const&);
    virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
    virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
    
};


GenParticleSelectorAMCatNLO::GenParticleSelectorAMCatNLO(const edm::ParameterSet& iConfig)
{
    produces<std::vector<GenParticle>>("trueTop");
    produces<std::vector<GenParticle>>("trueLightJet");
    produces<std::vector<GenParticle>>("trueBJet");
    produces<std::vector<GenParticle>>("trueLepton");
    produces<std::vector<GenParticle>>("trueNeutrino");
    produces<std::vector<GenParticle>>("trueWboson");
    produces<int>("trueLeptonPdgId");
    
    _srcTag = iConfig.getParameter<edm::InputTag>("src");
    
}


GenParticleSelectorAMCatNLO::~GenParticleSelectorAMCatNLO()
{
    
    // do anything here that needs to be done at desctruction time
    // (e.g. close files, deallocate resources etc.)
    
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
GenParticleSelectorAMCatNLO::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

    Handle<GenParticleCollection> genParticles;
    iEvent.getByLabel(_srcTag, genParticles);

    std::auto_ptr<std::vector<GenParticle> > outLightJets(new std::vector<GenParticle>());
    std::auto_ptr<std::vector<GenParticle> > outBJets(new std::vector<GenParticle>());
    std::auto_ptr<std::vector<GenParticle> > outLeptons(new std::vector<GenParticle>());
    std::auto_ptr<std::vector<GenParticle> > outNeutrinos(new std::vector<GenParticle>());
    std::auto_ptr<std::vector<GenParticle> > outWbosons(new std::vector<GenParticle>());
    std::auto_ptr<std::vector<GenParticle> > outTop(new std::vector<GenParticle>());
    
    const GenParticle* lightJet = nullptr;
    const GenParticle* bJet = nullptr;
    const GenParticle* lepton = nullptr;
    const GenParticle* neutrino = nullptr;
    const GenParticle* wBoson = nullptr;
    const GenParticle* top = nullptr;
    
    for(size_t iparticle = 0; iparticle < genParticles->size(); ++ iparticle) 
    {
        const GenParticle& p = (*genParticles)[iparticle];
        const GenParticle* mom = (GenParticle*)p.mother( 0 );

        /* debug
        if ((abs(p.pdgId()) >= 11 and abs(p.pdgId()) <= 16) || abs(p.pdgId()) == 6 || abs(p.pdgId()) == 24 || abs(p.pdgId())<6)
        {
            LogDebug("part") << p.pdgId() << " " << p.status() << "\t" << mom->pdgId() << " " << mom->status();
            
            for(size_t mi = 0; mi < p.numberOfMothers(); ++ mi){
                GenParticle* mp = (GenParticle*) p.mother(mi);
                LogDebug("part") << "m " << mp->pdgId() << " " << mp->status();     
            }
            for(size_t mi = 0; mi < p.numberOfDaughters(); ++ mi){
                GenParticle* mp = (GenParticle*) p.daughter(mi);
                LogDebug("part") << "d " << mp->pdgId() << " " << mp->status();
            }
        }*/
                 
        if (((abs(p.pdgId())==11) or (abs(p.pdgId())==13)) && p.status() == 1)
        {
            if (abs(mom->pdgId()) == 24 && (mom->status() == 22 || mom->status() == 52))
            {
                outLeptons->push_back(p);
                lepton=&p;
            }
            else if(mom->pdgId() == p.pdgId())
            {   
                //Go up the decay chain until you find a mother that is a W             
                GenParticle* p1 = (GenParticle*)p.mother(0);
                GenParticle* p_mom = (GenParticle*)p1->mother( 0 );
                while(p_mom->pdgId() == p.pdgId())
                {
                    if(p_mom->numberOfMothers() > 0)
                    {   
                        p_mom = (GenParticle*)p_mom->mother( 0 );
                        p1 = (GenParticle*)p1->mother(0);
                    }
                }
                if(p_mom->pdgId() == 24 && (p_mom->status() == 22 || p_mom->status() == 52) && p1->status() == 23)
                {
                    outLeptons->push_back(p);
                    lepton=&p;
                }     
            }
        }
        
        if (((abs(p.pdgId())==12) or (abs(p.pdgId())==14)) && p.status() == 1)
        {
            const GenParticle* grandma = (GenParticle*)mom->mother( 0 );
            //if  ((mom->pdgId() == p.pdgId() && mom->status() == 23) || (grandma->pdgId() == p.pdgId() && grandma->status() == 23))
            if ((mom->pdgId() == p.pdgId() && mom->status() == 23) || (abs(mom->pdgId()) == 24 && mom->status() == 52) || (abs(grandma->pdgId()) == 24 && grandma->status() == 52) || (abs(mom->pdgId()) == 24 && mom->status() == 22 && abs(grandma->pdgId()) == 6 && grandma->status() == 62))
            {
                outNeutrinos->push_back(p);
                neutrino=&p;
            }
        }
        
        if (abs(p.pdgId())==15 && p.status() == 2)
        {
            if( (abs(mom->pdgId()) == 24 && (mom->status() == 52 || mom->status() == 22)) || 
                (mom->pdgId() == p.pdgId() && mom->status() == 23))
            {
                outLeptons->push_back(p);
                lepton=&p;
            }
            else if(mom->numberOfMothers() > 0)
            {
                const GenParticle* grandma = (GenParticle*)mom->mother( 0 );
                if(mom->pdgId() == p.pdgId() && mom->status() == 51 && grandma->pdgId() == p.pdgId() && grandma->status() == 23)
                {
                    outLeptons->push_back(p);
                    lepton=&p;
                }
            }            
        }
        
        if (abs(p.pdgId())==16 && p.status() == 1 && 
            ((abs(mom->pdgId()) == 24 && (mom->status() == 52 || mom->status() == 22)) || 
            (mom->pdgId() == p.pdgId() && mom->status() == 23 )))
        {
            outNeutrinos->push_back(p);
            neutrino=&p;
        }
        
        if ((abs(p.pdgId())<5) && p.status() == 23 && p.numberOfMothers() == 2)
        {
            const GenParticle* mom2 = (GenParticle*)p.mother( 1 );
            //This case for 2->2
            if((abs(mom->pdgId()) == 2 && mom2->pdgId() == 21) || (mom->pdgId() == 21 && abs(mom2->pdgId()) == 2))
            {
                //cout << "jet " << p.pdgId() << " " << mom->pdgId() << " " << mom->status() << endl;
                lightJet=&p;
            }
            else if(mom->numberOfDaughters() >= 3) //2->3
            {
                if(!lightJet)
                {
                    lightJet = &p;
                    LogDebug("part") << "jet " << p.pdgId() << " " << mom->pdgId() << " " << mom->status();                
                
                }
                if(abs(p.pdgId()) < abs(lightJet->pdgId()))
                {
                    lightJet = &p;
                    LogDebug("part") << "jet " << p.pdgId() << " " << mom->pdgId() << " " << mom->status();                
                }
            }
        }

        if ((abs(p.pdgId()) == 5) && p.status() == 23 && p.numberOfMothers() == 1)
        {
            outBJets->push_back(p);
            bJet=&p;
        }
        
        if ((abs(p.pdgId()) == 24))
        {
            const GenParticle* dau = (GenParticle*)p.daughter( 0 );
            //second case when status 22 W decays directly without status 52 W
            if(dau->pdgId() != 24
                && ((p.status() == 52 && p.numberOfMothers() == 1) 
                    || (p.status() == 22 && abs(mom->pdgId()) == 6 && mom->status() == 62)))
            {
                outWbosons->push_back(p);
                wBoson=&p;
            }
        }
        if (abs(p.pdgId()) == 6 && p.status() == 62 )
        {
            outTop->push_back(p);
            top=&p;
        }
        
    }
                
    if (!lightJet)
    {
        LogWarning("light jet not found in current event");
        iEvent.put(outLeptons, "trueLepton");
        iEvent.put(outLightJets, "trueLightJet");
        iEvent.put(outBJets, "trueBJet");
        iEvent.put(outNeutrinos, "trueNeutrino");
        iEvent.put(outWbosons, "trueWboson");
        iEvent.put(outTop,"trueTop");
        iEvent.put(std::auto_ptr<int>(new int(0)), "trueLeptonPdgId");
        return;
    }

    outLightJets->push_back(*lightJet);
    

    if (!lepton || !neutrino || !top || !wBoson || !bJet)
    {
        LogWarning("lepton, neutrino, W, top or b-jet not found in current event");
        cout << lepton << " " << neutrino << " " << " " << wBoson << " " << top << " " << bJet << endl;
        iEvent.put(outLeptons, "trueLepton");
        iEvent.put(outLightJets, "trueLightJet");
        iEvent.put(outBJets, "trueBJet");
        iEvent.put(outNeutrinos, "trueNeutrino");
        iEvent.put(outWbosons, "trueWboson");
        iEvent.put(outTop,"trueTop");
        iEvent.put(std::auto_ptr<int>(new int(0)), "trueLeptonPdgId");
        return;
    }
    
    LogDebug("part") << "lepton " << lepton->p4(); 
    LogDebug("part") << "neutrino " << neutrino->p4(); 
    LogDebug("part") << "W " << wBoson->p4(); 
    LogDebug("part") << "bJet " << bJet->p4(); 
    LogDebug("part") << "top " << top->p4() << " m=" << top->mass(); 
    
    iEvent.put(outLeptons, "trueLepton");
    iEvent.put(outLightJets, "trueLightJet");
    iEvent.put(outBJets, "trueBJet");
    iEvent.put(outNeutrinos, "trueNeutrino");
    iEvent.put(outWbosons, "trueWboson");
    iEvent.put(outTop,"trueTop");
    iEvent.put(std::auto_ptr<int>(new int(lepton->pdgId())), "trueLeptonPdgId");
    
}

// ------------ method called once each job just before starting event loop  ------------
void
GenParticleSelectorAMCatNLO::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
GenParticleSelectorAMCatNLO::endJob() {

}

// ------------ method called when starting to processes a run  ------------
void
GenParticleSelectorAMCatNLO::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void
GenParticleSelectorAMCatNLO::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void
GenParticleSelectorAMCatNLO::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void
GenParticleSelectorAMCatNLO::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
GenParticleSelectorAMCatNLO::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
    //The following says we do not know what parameters are allowed so do no validation
    // Please change this to state exactly what you do use, even if it is no parameters
    edm::ParameterSetDescription desc;
    desc.setUnknown();
    descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(GenParticleSelectorAMCatNLO);
