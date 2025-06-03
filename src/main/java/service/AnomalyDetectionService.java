package com.yourpackage.service;

import com.yourpackage.model.SQLQuery;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class AnomalyDetectionService {

    private final String PYTHON_API_URL = "http://localhost:5000/predict";

    public AnomalyResult detectAnomaly(SQLQuery query) {
        RestTemplate restTemplate = new RestTemplate();
        // Send the SQL query to the Flask API and get the anomaly detection result
        return restTemplate.postForObject(PYTHON_API_URL, query, AnomalyResult.class);
    }
}
