#include <DataFormats/Candidate/interface/CompositeCandidate.h>
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/JetReco/interface/Jet.h"

using namespace reco;

bool isGoodJet(reco::Jet jet)
{
    return (jet.pt() > 40 && fabs(jet.eta()) < 4.5);
}

bool isBTag()
{
    return false;
}

float deltaR(reco::CompositeCandidate p1, reco::CompositeCandidate p2)
{
    return reco::deltaR(p1.eta(), p1.phi() , p2.pt() , p2.phi());
}

