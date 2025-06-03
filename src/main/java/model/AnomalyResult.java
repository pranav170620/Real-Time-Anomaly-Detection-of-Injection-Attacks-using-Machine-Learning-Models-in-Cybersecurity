package com.yourpackage.model;

public class AnomalyResult {
    private String decisionTreePrediction;
    private String randomForestPrediction;
    private String consequence;
    private String insight;
    private String riskLevel;

    // Getter and Setter for decisionTreePrediction
    public String getDecisionTreePrediction() {
        return decisionTreePrediction;
    }

    public void setDecisionTreePrediction(String decisionTreePrediction) {
        this.decisionTreePrediction = decisionTreePrediction;
    }

    // Getter and Setter for randomForestPrediction
    public String getRandomForestPrediction() {
        return randomForestPrediction;
    }

    public void setRandomForestPrediction(String randomForestPrediction) {
        this.randomForestPrediction = randomForestPrediction;
    }

    // Getter and Setter for consequence
    public String getConsequence() {
        return consequence;
    }

    public void setConsequence(String consequence) {
        this.consequence = consequence;
    }

    // Getter and Setter for insight
    public String getInsight() {
        return insight;
    }

    public void setInsight(String insight) {
        this.insight = insight;
    }

    // Getter and Setter for riskLevel
    public String getRiskLevel() {
        return riskLevel;
    }

    public void setRiskLevel(String riskLevel) {
        this.riskLevel = riskLevel;
    }
}