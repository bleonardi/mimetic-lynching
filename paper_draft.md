# Mimetic Contagion and Collective Violence: Spatial Evidence from Lynching in the US Cotton Belt, 1884–1936

**Draft — Do Not Cite Without Permission**

---

## Abstract

René Girard's theory of mimetic contagion proposes that collective violence spreads through social imitation: communities observe neighboring communities' scapegoating and reproduce it, independently of their own grievances. We test this mechanism using a county-year panel of 609 Black lynching victims in the US Cotton Belt from 1884 to 1936. Estimating a spatial lag model with two-way fixed effects (county and year), we find that a one-unit increase in neighboring counties' lagged lynching rate raises the probability of a lynching in the focal county by 6.7 percentage points (ρ = +0.067, p = 0.006). By contrast, the arrival of the boll weevil — the canonical economic disruption instrument in this literature — has a statistically insignificant effect (β = +0.003, p = 0.138), as does its interaction with cotton price declines (p = 0.651). These results hold after absorbing all time-invariant county characteristics and common annual shocks. The spatial lag effect is consistent with mimetic contagion — the signature of imitative propagation predicted by Girardian theory — while the economic shock evidence suggests that disruption may activate but does not propagate collective violence. The failure of the boll weevil as an instrumental variable for the spatial lag (first-stage F = 0.37) reflects the fundamental identification challenge: the weevil's slow geographic diffusion covaries with the very social network through which mimesis operates. We discuss better instruments and the broader methodological contribution of spatial weight matrices as tools for modeling any contagion network — geographic, informational, or institutional.

**Keywords:** lynching, mimetic contagion, spatial econometrics, boll weevil, racial violence, Girard

---

## 1. Introduction

The literature on racial lynching in the American South has largely organized itself around two explanatory frameworks. The first is economic: lynching served as a mechanism of labor control and economic competition management, with violence rising when Black economic progress threatened white economic position or when commodity shocks created material grievances in need of a scapegoat (Tolnay & Beck, 1995; Soule, 1992). The second is demographic: the "racial threat" hypothesis holds that lynching was more frequent in counties with higher Black population shares, where white communities perceived greater threat to social hierarchy (Bailey, Duchscherer & Grant, 2017; Blumer, 1958). Both frameworks treat lynching as a locally determined response to locally determined conditions.

What these frameworks largely elide is the mechanism of propagation. Even granting that economic distress or demographic threat creates a *disposition* toward collective violence, these conditions do not explain why the specific form that violence takes — the public lynching, the crowd, the ritual humiliation — spreads spatially and temporally across communities. Communities facing identical economic or demographic conditions do not all lynch at equal rates. And communities that lynch in one year are more likely to have neighbors that lynch in subsequent years, a pattern that economic and demographic models struggle to accommodate.

René Girard's theory of mimetic contagion offers a different account. In Girard's framework, mimetic desire — the tendency of human beings to model their desires and behaviors on those of others — produces rivalry and eventually collective violence when that rivalry reaches a crisis point (Girard, 1977). The resolution of mimetic crisis through the scapegoating mechanism — the collective expulsion or destruction of a surrogate victim — is itself mimetically transmitted: communities learn from neighboring communities that collective violence is available as a social technology for restoring order (Girard, 1986). On this account, the *propagation* of lynching should be spatially structured, with neighboring communities' histories predicting focal communities' behavior even after controlling for local conditions.

This paper provides the first systematic empirical test of the Girardian mimetic contagion hypothesis using quantitative spatial methods. We construct a county-year panel covering 1,201 counties in the US Cotton Belt from 1884 to 1936, drawing on the Seguin-Rigby lynching database (Seguin & Rigby, 2019), decennial census data interpolated annually from NHGIS, NBER cotton price series, reconstructed county cotton acreage, and a digitized version of the USDA boll weevil arrival map (Hunter & Coad, 1923). We estimate a spatial lag model with two-way fixed effects, in which the weighted average of neighboring counties' prior-year lynching enters as a right-hand-side variable. The coefficient on this spatial lag, ρ, is our empirical signature of mimetic contagion.

The main finding is stark: ρ = +0.067 (SE = 0.025, p = 0.006). Neighboring counties' prior-year lynching strongly predicts focal county lynching, even after absorbing all time-invariant county characteristics and all common annual shocks. This effect is substantively significant: at a baseline lynching rate of 0.49%, a one-unit increase in the spatial lag — roughly, one or more adjacent counties having a lynching event the prior year — raises the probability of a lynching by 6.7 percentage points, a more than thirteenfold increase over the baseline. The boll weevil shock, by contrast, has an economically small and statistically insignificant effect. The mimetic spillover is the more robust predictor.

These results contribute to several literatures. To the lynching literature, they add a spatial-contagion dimension that complements existing economic and demographic accounts. To the broader literature on collective violence, they suggest that standard models omitting network effects may systematically misattribute the drivers of violence. To the methodological literature on spatial econometrics, we discuss how weight matrices designed for geographic adjacency can be repurposed for any contagion network — railroad connections, newspaper co-circulation zones, denominational networks — providing sharper tests of informational versus geographic mimesis. And to the theoretical literature engaging with Girard, this paper offers a quantitative formalization and test of mechanisms that have heretofore been discussed only at the level of historical narrative or case study.

The paper proceeds as follows. Section 2 reviews the relevant theoretical and empirical literature. Section 3 describes the data. Section 4 presents the econometric model. Section 5 reports results. Section 6 discusses identification, limitations, and extensions. Section 7 concludes.

---

## 2. Theoretical Background and Literature Review

### 2.1 Girardian Mimetic Theory

Girard's account of collective violence begins with mimetic desire: human beings do not desire autonomously but rather imitate the desires of others, taking their models from those around them. This mimetic structure is productive of rivalry — when two parties desire the same object because each takes the other as a model, they become doubles, and the rivalry escalates. When mimetic rivalry spreads through a community, it produces an undifferentiated crisis of violence and contagion. The resolution of this crisis is the scapegoating mechanism: the community converges on a single victim — typically marked as marginal, different, or guilty in some respect — and expels or destroys that victim collectively. The collective violence restores social peace, at least temporarily, by redirecting the mimetic rivalry onto a single object (Girard, 1977).

Crucially for our purposes, the scapegoating mechanism is itself mimetically transmitted. Communities learn from neighboring communities that this technology of violence is available. The specific form that scapegoating takes — who is eligible as victim, what rituals attend the violence, how the community assembles — is transmitted through observation and imitation. This transmission is spatial: communities are more likely to learn from geographically proximate communities with whom they share social ties, common media, and interpersonal networks. The Girardian prediction is therefore not merely that lynching will occur when communities face economic or demographic stress, but that the occurrence of lynching in one community will propagate to neighboring communities through mimetic contagion, independently of those neighbors' own economic or demographic conditions.

This is a strong and testable prediction. It implies a positive spatial autocorrelation in lynching that persists after controlling for common shocks (absorbed by year fixed effects) and local characteristics (absorbed by county fixed effects). The coefficient ρ on the spatial lag of neighboring counties' prior-year lynching is precisely the quantity that would be zero under purely local determination and positive under mimetic contagion.

### 2.2 Economic Accounts: The Boll Weevil and Cotton Prices

The canonical economic account of lynching in the Cotton Belt centers on the disruption of the cotton economy. Tolnay and Beck (1995) document that lynching rates were higher when cotton prices were low, consistent with the thesis that economic frustration generated by commodity market downturns was displaced onto Black victims. More recently, Lange, Olmstead and Rhode (2009) use the sequential geographic arrival of the boll weevil — a crop pest whose northwestward march from Texas destroyed cotton crops across the South between roughly 1895 and 1920 — as a plausibly exogenous shock to local economic conditions, finding large effects on Black out-migration. The boll weevil's geographic diffusion path, determined by ecological rather than social factors, provides an instrument for local economic disruption that is conceptually independent of local racial attitudes.

We incorporate both cotton prices and boll weevil arrival in our specification. The interaction of post-weevil status with cotton price declines captures the joint economic crisis — weevil arrival exacerbating the damage from low prices — that the economic literature posits as the proximate cause of racial violence. Our central question is whether this economic disruption channel remains after we condition on the spatial lag of neighboring counties' lynching. The answer, as we will show, is that the economic disruption effects are economically small and statistically insignificant while the spatial lag remains large and significant.

### 2.3 Demographic Accounts: Racial Threat

The racial threat hypothesis, developed in the sociology literature by Blumer (1958) and applied to lynching by Bailey, Duchscherer and Grant (2017) among others, proposes that lynching was more frequent in counties where white communities felt more demographically threatened — operationalized as higher Black population share. The mechanism is one of group position: white violence is a technology for enforcing racial hierarchy, and the incentive for that violence is higher where the perceived threat to hierarchy is greater. We include Black population share as a control variable, and we find a positive and statistically significant effect (β = +0.022, p = 0.036), consistent with the racial threat account. The spatial lag, however, remains significant after absorbing this demographic mechanism, indicating that mimetic contagion operates over and above the racial threat channel.

### 2.4 Spatial Approaches to Collective Violence

Spatial methods have been used in the collective violence literature, but rarely with explicit theoretical grounding in contagion mechanisms. Soule (1992) documented spatial clustering of lynching without modeling the propagation process. More recent work on riots, coups, and civil conflict has used spatial lag models to test for diffusion effects (e.g., Braithwaite, 2010), but the theoretical framing typically remains at the level of "diffusion" without specifying the social mechanism. Our contribution is to connect the spatial econometric structure explicitly to Girardian theory, in which the mechanism of mimetic contagion makes specific predictions about the spatial and temporal structure of the diffusion process.

---

## 3. Data

### 3.1 Lynching Incidents

Our primary outcome data come from the Seguin-Rigby lynching database (Seguin & Rigby, 2019), which compiles 1,328 confirmed lynching incidents in the United States between 1883 and 1936. This database represents the most comprehensive and carefully documented compilation available, reconciling earlier sources including the NAACP records, the Tuskegee Institute data, and Tolnay and Beck's (1995) earlier compilation. For our analysis, we restrict attention to incidents with Black victims occurring in counties within the Cotton Belt — the tier of states where cotton production was economically dominant and where the boll weevil's impact was most consequential. After applying these restrictions, our sample includes 609 lynching incidents, distributed across 1,201 counties over 53 years (1884–1936).

The outcome variable L_it is a binary indicator equal to one if county i experienced at least one lynching in year t. We use a binary indicator rather than a count because the vast majority of county-years with any lynching have exactly one incident, and a linear probability model with a binary outcome facilitates interpretation of the spatial lag coefficient. The baseline lynching rate in the sample is 0.49%: 312 of 63,667 county-year observations record a lynching.

### 3.2 Population and Racial Composition

County-level demographic data come from the NHGIS full-count decennial censuses for 1880, 1890, 1900, 1910, 1920, and 1930. We interpolate linearly between census years to construct annual estimates of total county population and Black population share for each year in our panel. This interpolation introduces classical measurement error that will, if anything, attenuate our coefficient estimates. Black population share — our proxy for the racial threat mechanism — ranges from near zero in the northern fringe of the Cotton Belt to over 70% in the Mississippi Delta counties.

### 3.3 Cotton Prices

Annual average cotton prices come from the NBER Macrohistory Database, constructed from monthly spot price series for cotton at New Orleans. We convert monthly prices to annual averages and express them in nominal terms, consistent with the interpretation that contemporaneous price signals drove local behavior. Cotton price declines are operationalized as year-over-year percentage decreases in the annual average. We interact price declines with post-weevil arrival status to capture the double economic crisis predicted by the economic disruption hypothesis.

### 3.4 Boll Weevil Arrival

The boll weevil (*Anthonomus grandis*) entered the United States from Mexico near Brownsville, Texas around 1892 and spread northeastward, reaching the Atlantic coast by approximately 1921. County-level arrival years are derived from the USDA map published by Hunter and Coad (1923), which provides isochrone lines indicating when the weevil's infestation front crossed each region. We digitized this map and used radial basis function (RBF) interpolation to assign arrival years to 1,204 county centroids. PostWeevil_it is a binary indicator equal to one for all years at or after the interpolated arrival year for county i. The digitization and interpolation process introduces geographic measurement error that is plausibly independent of our outcome variable conditional on location.

### 3.5 Spatial Weight Matrix

The spatial weight matrix W is constructed from the Census Bureau county adjacency file, which records 18,967 pairs of contiguous county pairs based on 2010 boundaries. We apply this adjacency structure to our historical panel under the assumption that county boundary changes between the 1880s and 1930s did not substantially alter the adjacency network. The weight matrix is row-standardized so that each row sums to one, meaning the spatial lag W·L_{j,t-1} represents the average prior-year lynching rate among county i's neighbors. This is the standard specification in the spatial econometrics literature (Anselin, 1988) and ensures that the coefficient ρ is directly interpretable as the effect of a one-unit increase in the average neighbor lynching rate.

A key limitation is that 2010 boundaries are used to proxy for late 19th and early 20th century adjacency relationships. County boundary changes over this period were substantial in some states — particularly in Texas, where many counties were created from large western tracts. We assess robustness by restricting to counties whose boundaries were stable by 1900, and find qualitatively similar results.

### 3.6 Summary Statistics

The 63,667 county-year observations span 1,201 counties across 53 years. The average county-year has a Black population share of 28.4%, a log population of 9.3 (approximately 11,000 residents), and a post-weevil indicator that is zero for approximately 61% of observations. The spatial lag — the average neighbor prior-year lynching indicator — has a mean of 0.008, reflecting the relative rarity of lynching events in any given county-year. The standard deviation of the spatial lag (0.034) is more than four times its mean, indicating substantial cross-sectional and temporal variation in the neighborhood lynching environment.

---

## 4. Model

### 4.1 Empirical Specification

The primary estimating equation is a linear probability model with spatial lag and two-way fixed effects:

$$L_{it} = \rho \cdot \sum_j w_{ij} L_{j,t-1} + \beta \cdot \text{PostWeevil}_{it} + \gamma \cdot (\text{PostWeevil}_{it} \times \text{CottonPriceDecline}_t) + \delta \cdot \text{BlackShare}_{it} + \lambda \cdot \log \text{Pop}_{it} + \alpha_i + \tau_t + \varepsilon_{it}$$

where $w_{ij}$ are elements of the row-standardized weight matrix W, $\alpha_i$ are county fixed effects, $\tau_t$ are year fixed effects, and $\varepsilon_{it}$ is an idiosyncratic error term. Standard errors are HC3 heteroskedasticity-robust, clustered at the county level to account for serial correlation in within-county errors.

The county fixed effects $\alpha_i$ absorb all time-invariant county characteristics — geography, soil quality, antebellum plantation legacy, proximity to markets, political culture — that might confound the relationship between local conditions and lynching. The year fixed effects $\tau_t$ absorb all common annual shocks, including national commodity price movements, political events, and the aggregate time trend in lynching rates. Identification of ρ therefore comes from variation in neighbor lynching rates that is not explained by common annual shocks or time-invariant county characteristics: within-county deviations from county means that are correlated with within-county deviations in neighbor lynching rates from their respective county means.

### 4.2 The Spatial Lag as Mimetic Contagion

The spatial lag $\sum_j w_{ij} L_{j,t-1}$ is the row-standardized average of neighboring counties' prior-year lynching. We use a one-year lag rather than contemporaneous values for two reasons. First, it resolves the reflection problem (Manski, 1993): contemporaneous spatial lags are mechanically correlated with contemporaneous disturbances if there are common shocks, whereas a lagged spatial lag is predetermined with respect to current period shocks. Second, the Girardian mechanism operates through a temporal sequence: a community observes a neighboring community's lynching, the observation propagates through social networks, and the mimetic contagion eventually produces a lynching in the observing community. This transmission takes time, and a one-year lag is a reasonable window for that process.

The coefficient ρ captures the mimetic contagion effect: the increase in the probability of a lynching in county i in year t associated with a one-unit increase in the average lynching rate among county i's neighbors in year t-1. Under the null hypothesis of purely local determination, ρ = 0. Under the Girardian hypothesis of mimetic contagion, ρ > 0.

### 4.3 Economic Disruption Variables

PostWeevil_it captures the post-arrival period for county i, during which the boll weevil infestation disrupted cotton production. The coefficient β measures the average effect of boll weevil arrival on lynching probability, holding fixed county and year effects. The interaction CottonPriceDecline_t × PostWeevil_it captures whether the combination of weevil infestation and falling cotton prices — the joint economic crisis condition — raises lynching probability above the individual effects of either shock. Under the economic disruption hypothesis, we expect β > 0 and γ > 0.

### 4.4 Instrumental Variables Approach

We attempted to instrument the spatial lag with the share of neighboring counties that had experienced boll weevil arrival in the prior year (neighbor post-weevil share, lagged one year). The logic of this instrument is that weevil-induced economic distress in neighboring counties would affect neighbors' lynching rates (which then affect focal county lynching through the spatial lag) but would not directly affect focal county lynching beyond the focal county's own weevil status. 

The first-stage F-statistic was 0.37, indicating a severely weak instrument. We therefore do not report IV estimates as our main results, though the OLS spatial lag estimate is our preferred specification given the richness of the fixed effects structure. We discuss the failure of this instrument and propose better alternatives in Section 6.

---

## 5. Results

### 5.1 Main Results

Table 1 reports the main results from the two-way fixed effects spatial lag model.

**Table 1: Spatial Lag Model of Lynching, Cotton Belt Counties 1884–1936**

| Variable | Coefficient | Std. Error | p-value |
|---|---|---|---|
| Spatial lag (neighbor lynching, t−1) | +0.0667 | 0.0245 | 0.006 |
| Post boll weevil arrival | +0.0028 | 0.0019 | 0.138 |
| Weevil × cotton price decline | +0.0005 | 0.0010 | 0.651 |
| Black population share | +0.0215 | 0.0102 | 0.036 |
| Log population | +0.0009 | 0.0004 | 0.050 |

*N = 63,667 county-years. 1,201 counties, 53 years. County and year fixed effects absorbed. HC3 robust standard errors. Base lynching rate = 0.49%.*

The spatial lag coefficient is +0.0667 (SE = 0.025, p = 0.006). This is both statistically significant and substantively large relative to the baseline. At a baseline lynching rate of 0.49%, the 6.7 percentage point increase associated with a one-unit increase in the spatial lag represents more than a thirteenfold increase in the lynching probability. A one-unit increase in the spatial lag corresponds to all of a county's neighbors having had a lynching in the prior year — an extreme counterfactual, but one that illustrates the magnitude of the estimated effect. More practically, moving from zero to one neighbor with a prior-year lynching, for a county with four neighbors, increases the spatial lag by 0.25, which corresponds to a 1.7 percentage point increase in the lynching probability — a 3.5-fold increase over baseline.

The boll weevil arrival coefficient is +0.0028 (SE = 0.0019, p = 0.138). This is statistically indistinguishable from zero at conventional significance levels. The point estimate is positive, consistent with the directional prediction of the economic disruption hypothesis, but the confidence interval encompasses values close to zero. The interaction of weevil arrival with cotton price declines is even smaller in magnitude and statistically insignificant (β = +0.0005, p = 0.651). Together, these results provide little support for the economic disruption mechanism as a direct driver of lynching, at least within the two-way fixed effects framework that absorbs county-specific baseline levels and common annual shocks.

Black population share is positive and statistically significant (β = +0.022, p = 0.036), consistent with the racial threat hypothesis. Counties with higher Black population shares had higher lynching rates, a finding robust to the inclusion of the spatial lag. Log population is also positive and marginally significant (β = +0.0009, p = 0.050), which may reflect greater opportunity for crowd formation in larger counties or may partly capture urbanization effects.

### 5.2 The Spatial Lag as the Primary Driver

A key interpretive question is whether the spatial lag is absorbing omitted local economic or demographic variables rather than capturing genuine mimetic contagion. Several features of the results argue against this concern. First, the spatial lag is robust to inclusion of county fixed effects, which absorb any time-invariant confounders. A county with persistently high economic distress and persistently high lynching rates would be absorbed by the county fixed effect; the spatial lag captures *deviations* from that county's typical pattern that are correlated with neighbor deviations. Second, the year fixed effects absorb any common shocks — including national commodity price movements — that might simultaneously raise lynching rates across neighboring counties. Third, the boll weevil arrival variable is included explicitly to capture local economic disruption, and it enters with an insignificant coefficient, suggesting that local economic conditions beyond the county average and national trends do not explain the spatial lag's effect.

### 5.3 Girard-Specific Prediction: Crisis Activation of Contagion

Girardian theory makes a specific prediction beyond simply ρ > 0: the mimetic contagion should be stronger during periods of economic crisis, when communities are already in the scapegoating mindset and more susceptible to mimetic influence. We test this by interacting the spatial lag with an indicator for post-weevil arrival and with cotton price decline indicators. These interaction results are suggestive: the spatial lag coefficient is somewhat larger in post-weevil county-years (ρ = +0.081 versus ρ = +0.052 in pre-weevil years), though the interaction is not statistically distinguishable from zero at conventional significance levels (p = 0.21). This directional pattern is consistent with the Girardian prediction but underpowered: the relatively small number of post-weevil lynching events limits the precision of this subgroup analysis. Future work with richer data on local economic conditions might better test this interaction.

---

## 6. Discussion

### 6.1 Interpretation of the Spatial Lag

The spatial lag coefficient ρ = +0.067 is our central finding, and its interpretation requires care. The coefficient captures the association between prior-year neighbor lynching and current focal county lynching, after absorbing county and year fixed effects. Under the assumption that the error term is uncorrelated with the lagged spatial lag — which the two-way FE structure makes plausible, since common shocks and time-invariant local characteristics are absorbed — this coefficient has a causal interpretation as the effect of neighbor lynching on focal county lynching. The mechanism we propose, following Girard, is mimetic: communities observe neighboring communities' collective violence and reproduce it through social imitation.

Alternative mechanisms should be considered. One possibility is that the spatial lag captures a network spillover of economic conditions not fully absorbed by the boll weevil variable and the year fixed effects — for example, local commodity price variation driven by regional market integration. However, the inclusion of county-specific boll weevil timing and national cotton prices already captures the main sources of local economic variation. Another possibility is that the spatial lag captures a common-shock mechanism operating at sub-national scale — for example, regional newspaper coverage of a lynching that incites further violence across a multi-county readership area. This mechanism is not strictly inconsistent with Girardian theory (newspaper coverage is itself a mimetic transmission channel), but it would blur the distinction between geographic and informational mimesis that our design cannot resolve.

### 6.2 Why the IV Fails

The failure of the boll weevil instrument (first-stage F = 0.37) reflects a fundamental mismatch between the identification strategy and the quantity we seek to identify. The boll weevil spread from southwest to northeast across the Cotton Belt over roughly 25 years, following a wave front determined by ecological and climatic factors. This geographic diffusion pattern is slow and spatially smooth: counties entered the post-weevil period in geographic sequence, and their neighbors typically entered within one to three years. The neighbor post-weevil share therefore varies primarily along the wave front, with most counties having either all or none of their neighbors in the post-weevil period.

The problem is that the spatial lag we seek to instrument is precisely the average neighbor lynching rate, which varies within networks — between pairs of neighboring counties in the same wave-front region — much more than the boll weevil instrument does. The boll weevil instrument predicts between-wave-front variation in neighbor economic distress, but does a poor job of predicting within-network variation in neighbor lynching. This is what the weak first stage reflects: the instrument lacks the within-network variation needed to identify the spatial lag.

Better instruments would exploit asymmetric local shocks that hit specific counties within a network but not their neighbors. Severe droughts, floods, or crop failures driven by idiosyncratic weather events would affect a single county's economic conditions — and thus potentially its lynching rate — without the slow geographic diffusion that afflicts the boll weevil. If such a county's elevated lynching rate then propagates to its neighbors (through the mimetic mechanism), the instrument — neighbor experiencing a local weather shock — would have power precisely in the variation we care about. County-level weather data from historical climate reconstructions would make this identification strategy feasible and would provide a considerably sharper test of the mimetic contagion hypothesis.

### 6.3 Methodological Contribution: Weight Matrices Beyond Geography

The spatial weight matrix W in our specification is defined by geographic adjacency, reflecting the assumption that the relevant social network for mimetic transmission is geographic proximity. This assumption is defensible for the period and context — in the late 19th and early 20th century American South, geographic proximity was the primary determinant of social networks, and information traveled through networks shaped by physical distance. But it is not the only possible assumption, and our findings suggest a productive research agenda in which alternative weight matrices are used to test different theories of mimetic transmission.

A denomination-based weight matrix, for example, would connect counties sharing the same dominant Protestant denomination, capturing the hypothesis that mimetic contagion traveled through church networks that organized community life in the rural South. A railroad-network weight matrix would connect counties linked by the same rail lines, testing whether faster information transmission accelerated mimetic contagion. A newspaper co-circulation weight matrix — connecting counties covered by the same regional newspapers, which prominently reported lynching events — would distinguish between informational mimesis (copying behavior you read about) and more direct social mimesis (copying behavior you observe in neighboring communities you interact with directly).

The advantage of the spatial lag framework is that it is fully agnostic about the structure of W; the same estimating equation accommodates any well-defined social network. The coefficient ρ would have different interpretations under different W specifications, but the identifying logic — conditioning on local characteristics and common shocks, asking whether network neighbors' prior violence predicts focal community violence — remains constant. This generality makes the spatial lag model a natural workhorse for testing contagion hypotheses across a wide range of social network structures.

### 6.4 The Economic Disruption Channel

The failure of the boll weevil variable to reach statistical significance requires interpretation. Two readings are possible. The first, consistent with Girardian theory, is that economic disruption is a *condition* for the scapegoating mechanism but not a direct cause: the weevil creates the crisis environment in which communities are susceptible to mimetic contagion, but the actual propagation occurs through imitation. Under this reading, the boll weevil effect should appear as an interaction with the spatial lag — crisis conditions amplifying the contagion — rather than as a main effect. The directional pattern in our subgroup analysis (larger ρ in post-weevil years) is consistent with this interpretation.

The second reading is that the boll weevil's effect on lynching, if any, is simply too small to detect given our sample size and the noise introduced by interpolating county-level arrival years. The Lange, Olmstead and Rhode (2009) finding of a large boll weevil effect on Black out-migration does not necessarily imply a large effect on lynching, which was a rarer event driven by more contingent factors. Our negative result on the boll weevil channel should be interpreted with appropriate humility: null results in panel models with many fixed effects and noisy instruments are common, and the directional positive coefficient is consistent with the economic disruption hypothesis even if imprecisely estimated.

### 6.5 Limitations

Several limitations of the current analysis deserve explicit acknowledgment.

**Interpolated population data.** Annual population and racial composition estimates are linearly interpolated from decennial census benchmarks. This introduces measurement error that is serially correlated within counties and potentially correlated with our regressors — the boll weevil, for example, induced substantial Black out-migration that would make post-weevil population counts increasingly inaccurate between census years. Classical measurement error in the population controls would attenuate their coefficients and potentially bias the spatial lag coefficient in either direction.

**Digitized boll weevil map.** The county-level weevil arrival years are derived from a 1923 USDA map via digitization and RBF interpolation. The original map represents contemporaneous expert knowledge of the weevil's spread and is almost certainly not perfectly accurate, particularly for early arrivals in the 1890s where documentation was sparser. RBF interpolation smooths across the county centroids, potentially misclassifying counties near the wave front. This measurement error is plausibly classical conditional on location, biasing the weevil coefficient toward zero — consistent with our finding of small, insignificant boll weevil effects.

**2010 county boundaries.** The spatial weight matrix is constructed from 2010 county adjacency relationships applied to a 1884–1936 panel. County boundary changes over this period, while substantial in some states, are unlikely to have dramatically altered the adjacency structure in the densely settled Cotton Belt states where most of our observations are concentrated.

**Binary outcome and linear probability model.** We use a linear probability model for computational tractability with large numbers of fixed effects. The LPM can produce fitted probabilities outside [0,1] and has known limitations with rare binary outcomes. A conditional logit or Poisson fixed effects model would be more appropriate in principle, and we note that implementing a spatial lag within a nonlinear fixed effects framework is an active area of methodological development. Given our very low base rate (0.49%), the LPM approximation is likely adequate for the main results but may affect subgroup analyses where predicted probabilities approach zero.

**Spatial weight matrix specification.** Our results are conditional on the choice of a geographic adjacency weight matrix. We have not systematically tested the robustness of ρ to alternative distance bands, kernel-weighted matrices, or network-based matrices. The robustness of the spatial lag result to these alternatives is an important open question.

---

## 7. Conclusion

This paper has provided the first quantitative test of Girard's theory of mimetic contagion applied to collective racial violence. Using a county-year panel of 609 Black lynching victims in the US Cotton Belt from 1884 to 1936, we estimated a spatial lag model with two-way fixed effects and found strong evidence of spatial contagion: neighboring counties' prior-year lynching raises the probability of a focal county lynching by 6.7 percentage points (ρ = +0.067, p = 0.006). This effect is robust to the inclusion of county and year fixed effects, demographic controls, and the canonical economic disruption variables from the lynching literature.

The boll weevil shock — the standard economic instrument in this literature — has a small and statistically insignificant direct effect on lynching in our specification (β = +0.003, p = 0.138). This finding does not necessarily refute the economic disruption hypothesis; it may reflect measurement error in the interpolated weevil arrival years or the genuinely moderate magnitude of economic disruption effects on rare events. What it does suggest is that the mimetic contagion channel, captured by the spatial lag, is a more robust predictor of lynching variation than local economic conditions as we measure them.

Taken together, these results support the Girardian account of collective violence not as a simple local response to local grievances, but as a socially reproduced practice that spreads through imitation. The scapegoating mechanism — the targeting of a vulnerable victim to resolve social tension — is not invented independently by each community; it is learned, observed, and copied. The spatial lag coefficient ρ is the empirical signature of this learning process.

The methodological contribution extends beyond this specific historical question. Spatial lag models with general weight matrices provide a flexible framework for testing any contagion hypothesis about collective behavior. The same estimating equation, with weight matrices defined by railroad networks, newspaper co-circulation zones, or denominational ties, could distinguish between informational and social mimesis, test whether the transmission medium matters, and ultimately shed light on the general mechanisms by which collective violence spreads — and, potentially, how it might be interrupted.

For scholars of historical racial violence, the findings underscore the importance of network effects in understanding why violence clustered in time and space beyond what local conditions would predict. For scholars of Girard, this paper offers what is to our knowledge the first systematic quantitative test of mimetic contagion in a well-documented historical case of collective violence, finding results broadly consistent with the theory's central predictions. The mechanism of scapegoating is social before it is local — learned before it is felt.

---

## References

Anselin, L. (1988). *Spatial Econometrics: Methods and Models*. Kluwer Academic Publishers.

Bailey, A., Duchscherer, K., & Grant, D. (2017). Targeting blacks: The killing fields of the Jim Crow South. *Ethnic and Racial Studies*, 40(12), 2106–2124.

Blumer, H. (1958). Race prejudice as a sense of group position. *Pacific Sociological Review*, 1(1), 3–7.

Braithwaite, A. (2010). Resisting infection: How state capacity conditions conflict contagion. *Journal of Peace Research*, 47(3), 311–319.

Girard, R. (1977). *Violence and the Sacred*. Johns Hopkins University Press.

Girard, R. (1986). *The Scapegoat*. Johns Hopkins University Press.

Hunter, W. D., & Coad, B. R. (1923). *The Boll Weevil: How to Combat It*. USDA Farmers' Bulletin 1329. United States Department of Agriculture.

Lange, M., Olmstead, A., & Rhode, P. (2009). The impact of the boll weevil, 1892–1932. *Journal of Economic History*, 69(3), 685–718.

Manski, C. F. (1993). Identification of endogenous social effects: The reflection problem. *Review of Economic Studies*, 60(3), 531–542.

Seguin, C., & Rigby, D. (2019). National crimes: A new national data set of lynchings in the United States, 1883 to 1941. *Socius*, 5, 1–9.

Soule, S. A. (1992). Populism and black lynching in Georgia, 1890–1900. *Social Forces*, 71(2), 431–449.

Tolnay, S. E., & Beck, E. M. (1995). *A Festival of Violence: An Analysis of Southern Lynchings, 1882–1930*. University of Illinois Press.
