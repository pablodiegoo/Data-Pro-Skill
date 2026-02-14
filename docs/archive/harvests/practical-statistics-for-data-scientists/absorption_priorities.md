# Harvest Absorption Priorities

**Date**: 2026-02-14  
**Total Items**: 43+  
**Target**: Data-Pro-Skill integration via `/project-evolution`

---

## Priority Matrix

### 🔴 HIGH PRIORITY (Immediate Value)

#### 1. Permutation Feature Importance ⭐⭐⭐⭐⭐
**File**: `scripts/permutation_feature_importance.py`  
**Target**: `data-analysis-suite` skill  
**Impact**: HIGH - Fills critical gap  
**Effort**: LOW - Drop-in utility  
**Reuse**: VERY HIGH - Applicable to all classification projects

**Why Now**:
- Works with ANY sklearn model (not just trees)
- More reliable than tree-based importance
- Essential for model interpretation
- No equivalent in Data-Pro-Skill

---

#### 2. Imbalanced Data Strategies Reference ⭐⭐⭐⭐⭐
**File**: `references/imbalanced_data_strategies.md`  
**Target**: `.agent/references/` in Data-Pro-Skill  
**Impact**: HIGH - Common real-world problem  
**Effort**: LOW - Documentation only  
**Reuse**: VERY HIGH - Most classification projects

**Why Now**:
- Comprehensive guide (SMOTE, weighting, ensembles)
- Critical for production ML
- Well-documented with examples
- Immediate reference value

---

#### 3. Database Snippets (All 3 Cycles) ⭐⭐⭐⭐
**Files**: `database/new_snippets*.json`  
**Target**: `datapro` CLI database  
**Impact**: MEDIUM-HIGH - Reduces code duplication  
**Effort**: LOW - JSON merge  
**Reuse**: HIGH - Standard patterns

**Why Now**:
- ~22 new snippets across 3 cycles
- Covers gaps in current database
- Easy integration (JSON format)
- Immediate productivity boost

---

### 🟡 MEDIUM PRIORITY (Next Sprint)

#### 4. GLM Partial Residual Plot ⭐⭐⭐
**File**: `scripts/glm_partial_residual_plot.py`  
**Target**: `data-analysis-suite` skill  
**Impact**: MEDIUM - Specialized use case  
**Effort**: LOW - Standalone utility  
**Reuse**: MEDIUM - Logistic regression projects

**Why Later**:
- Complements existing OLS partial residuals
- Less frequently used than permutation importance
- Still valuable for classification diagnostics

---

#### 5. Correlation Ellipse Plot ⭐⭐⭐
**File**: `scripts/correlation_ellipse_plot.py`  
**Target**: `data-viz` skill  
**Impact**: MEDIUM - Niche visualization  
**Effort**: LOW - Standalone function  
**Reuse**: MEDIUM - Academic/publication use

**Why Later**:
- Unique but not essential
- Grayscale-friendly alternative to heatmaps
- Good for publications

---

#### 6. PCA Plotting Utilities ⭐⭐⭐
**File**: `scripts/principal_component_plotting.py`  
**Target**: `data-viz` skill  
**Impact**: MEDIUM - Common in dimensionality reduction  
**Effort**: LOW - Visualization helpers  
**Reuse**: MEDIUM - PCA projects

---

### 🟢 LOW PRIORITY (Future Enhancement)

#### 7. Gower Distance Utility ⭐⭐
**File**: `scripts/gower_distance_utility.py`  
**Target**: New "clustering" skill or `data-analysis-suite`  
**Impact**: LOW-MEDIUM - Specialized clustering  
**Effort**: MEDIUM - Requires testing  
**Reuse**: LOW - Mixed-type clustering only

**Why Later**:
- Niche use case (mixed categorical/numeric)
- Not in sklearn (manual implementation)
- Requires more validation

---

#### 8. Multivariate Normal Contours ⭐⭐
**File**: `scripts/multivariate_normal_contours.py`  
**Target**: `data-viz` skill  
**Impact**: LOW - Theoretical/educational  
**Effort**: LOW - Standalone  
**Reuse**: LOW - Mostly teaching

---

#### 9. Permutation Test Utilities ⭐⭐
**File**: `scripts/permutation_test_utilities.py`  
**Target**: `data-analysis-suite` skill  
**Impact**: LOW - Educational reference  
**Effort**: LOW - Already generic  
**Reuse**: LOW - Mostly A/B testing

**Why Later**:
- Educational implementation
- scipy.stats has similar functionality
- Good reference but not critical

---

#### 10. Data Directory Finder ⭐
**File**: `scripts/data_directory_finder.py`  
**Target**: `data-pro-max` utilities  
**Impact**: LOW - Convenience utility  
**Effort**: LOW - Simple function  
**Reuse**: MEDIUM - Project setup

---

## Recommended Absorption Sequence

### Week 1: Quick Wins
1. ✅ Merge all database snippets → `datapro` CLI
2. ✅ Add `imbalanced_data_strategies.md` → `.agent/references/`
3. ✅ Integrate `permutation_feature_importance.py` → `data-analysis-suite`

**Effort**: 2-3 hours  
**Impact**: Immediate productivity boost

---

### Week 2: Core Utilities
4. ✅ Add `glm_partial_residual_plot.py` → `data-analysis-suite`
5. ✅ Add `principal_component_plotting.py` → `data-viz`
6. ✅ Add `correlation_ellipse_plot.py` → `data-viz`

**Effort**: 3-4 hours  
**Impact**: Completes core statistical toolkit

---

### Week 3: Specialized Tools (Optional)
7. ⚠️ Evaluate `gower_distance_utility.py` for clustering skill
8. ⚠️ Consider `multivariate_normal_contours.py` for teaching materials
9. ⚠️ Archive `permutation_test_utilities.py` as reference

**Effort**: 2-3 hours  
**Impact**: Niche enhancements

---

## Skill Creation Opportunities

### Option 1: "Classification Diagnostics" Skill
**Combine**:
- `glm_partial_residual_plot.py`
- `permutation_feature_importance.py`
- ROC/AUC snippets
- Confusion matrix utilities

**Value**: Unified classification workflow  
**Effort**: Medium (4-6 hours)

---

### Option 2: "Imbalanced Data Toolkit" Skill
**Combine**:
- `imbalanced_data_strategies.md` (reference)
- SMOTE/ADASYN snippets
- Class weighting utilities
- Evaluation metrics for imbalanced data

**Value**: End-to-end imbalanced data handling  
**Effort**: Medium (4-6 hours)

---

## Integration Checklist

For each item absorbed:
- [ ] Add to appropriate skill/reference
- [ ] Update skill SKILL.md documentation
- [ ] Add examples to skill
- [ ] Test with sample data
- [ ] Update `datapro` database (if applicable)
- [ ] Document in Data-Pro-Skill changelog

---

## Metrics for Success

**After Week 1**:
- [ ] 22+ new snippets in `datapro search`
- [ ] Imbalanced data guide accessible
- [ ] Permutation importance available in data-analysis-suite

**After Week 2**:
- [ ] All core statistical utilities integrated
- [ ] Visualization toolkit expanded
- [ ] Classification diagnostics complete

**After Week 3**:
- [ ] All high/medium priority items absorbed
- [ ] Documentation updated
- [ ] Skills tested and validated

---

## Risk Assessment

### Low Risk (Safe to Integrate)
- Database snippets (JSON merge)
- Reference documents (documentation)
- Standalone utilities (no dependencies)

### Medium Risk (Requires Testing)
- Gower distance (custom implementation)
- GLM partial residuals (statsmodels dependency)

### No Risk Identified
- All items are well-documented
- All items are generic (not project-specific)
- All items have clear use cases

---

## Final Recommendation

**Start with Week 1 priorities**:
1. Database snippets
2. Imbalanced data reference
3. Permutation importance

**Total effort**: 2-3 hours  
**Total impact**: Immediate and substantial

Then evaluate Week 2 based on:
- User feedback on Week 1 additions
- Demand for visualization utilities
- Time available for integration

---

**Next Action**: Run `/project-evolution` with focus on HIGH PRIORITY items
