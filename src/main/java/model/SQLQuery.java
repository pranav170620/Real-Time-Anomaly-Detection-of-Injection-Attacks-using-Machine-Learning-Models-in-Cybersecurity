package com.yourpackage.model;

public class SQLQuery {
    private String queryText;

    public SQLQuery() {}

    public SQLQuery(String queryText) {
        this.queryText = queryText;
    }

    public String getQueryText() {
        return queryText;
    }

    public void setQueryText(String queryText) {
        this.queryText = queryText;
    }
}