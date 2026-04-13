-- 1. Prix moyen au m² par département
SELECT 
    code_departement,
    AVG(prix_m2) as prix_moyen_m2,
    COUNT(*) as volume_ventes
FROM transactions_dvf
GROUP BY code_departement
ORDER BY prix_moyen_m2 DESC;

-- 2. Évolution du prix médian par année
SELECT 
    annee,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY prix_m2) as prix_median_m2
FROM transactions_dvf
GROUP BY annee
ORDER BY annee;

-- 3. Volume de transactions par mois
SELECT 
    annee,
    mois,
    COUNT(*) as volume_transactions
FROM transactions_dvf
GROUP BY annee, mois
ORDER BY annee, mois;

-- 4. Top 10 communes les plus chères
SELECT 
    code_departement,
    code_commune,
    AVG(prix_m2) as prix_moyen_m2
FROM transactions_dvf
GROUP BY code_departement, code_commune
HAVING COUNT(*) > 50  -- On filtre pour avoir une certaine significativité
ORDER BY prix_moyen_m2 DESC
LIMIT 10;

-- 5. Distribution des types de biens par région
SELECT 
    region,
    categorie_bien,
    COUNT(*) as nombre_biens
FROM transactions_dvf
GROUP BY region, categorie_bien
ORDER BY region, nombre_biens DESC;
