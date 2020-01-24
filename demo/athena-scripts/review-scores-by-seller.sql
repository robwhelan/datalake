SELECT order_reviews.order_id, orders.seller_id, review_score, sdr_id, sr_id
    FROM "2ndwatch-datalake-demo-datalake-raw-zone-database"."2ndwatch-datalake-demo_analytics_order_reviews" order_reviews
    join "2ndwatch-datalake-demo-datalake-raw-zone-database"."2ndwatch-datalake-demo_analytics_order_items" order_items
    on (order_reviews.order_id = order_items.order_id)
    join "2ndwatch-datalake-demo-datalake-raw-zone-database"."2ndwatch-datalake-demo_analytics_orders" orders
    on (order_items.seller_id = orders.seller_id)
limit 100;
