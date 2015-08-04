#ifndef UTILS_H
#define UTILS_H

#include <DataFormats/Candidate/interface/CompositeCandidate.h>
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/JetReco/interface/Jet.h"

using namespace reco;

bool isGoodJet(reco::Jet jet);
bool isBTag();
float deltaR(reco::CompositeCandidate p1, reco::CompositeCandidate p2);

#endif
