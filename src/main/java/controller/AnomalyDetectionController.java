package com.yourpackage.controller;

import com.yourpackage.model.SQLQuery;
import com.yourpackage.service.AnomalyDetectionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.validation.BindingResult;
import javax.validation.Valid;

@Controller
public class AnomalyDetectionController {

    @Autowired
    private AnomalyDetectionService anomalyDetectionService;

    @GetMapping("/")
    public String showDashboard(Model model) {
        model.addAttribute("query", new SQLQuery());
        return "dashboard";  // Thymeleaf template dashboard.html
    }

    @PostMapping("/detect")
    public String detectAnomaly(@Valid @ModelAttribute("query") SQLQuery query, BindingResult bindingResult, Model model) {
        if (bindingResult.hasErrors()) {
            return "dashboard";  // Return the dashboard with error messages
        }

        AnomalyResult result = anomalyDetectionService.detectAnomaly(query);

        if (result == null) {
            model.addAttribute("error", "An error occurred during anomaly detection. Please try again.");
            return "dashboard";
        }

        model.addAttribute("queryText", query.getQueryText());
        model.addAttribute("riskLevel", result.getRiskLevel());
        model.addAttribute("consequence", result.getConsequence());
        model.addAttribute("insight", result.getInsight());
        model.addAttribute("decisionTreePrediction", result.getDecisionTreePrediction());
        model.addAttribute("randomForestPrediction", result.getRandomForestPrediction());

        return "dashboard";  // Thymeleaf template dashboard.html
    }
}