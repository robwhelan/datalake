SELECT order_reviews.order_id, closed_deals.seller_id, review_score, sdr_id, sr_id
    FROM "datalake-demo-datalake-main-database"."datalake-demo_raw_order_reviews" order_reviews
    join "datalake-demo-datalake-main-database"."datalake-demo_raw_order_items" order_items
    on (order_reviews.order_id = order_items.order_id)
    join "datalake-demo-datalake-main-database"."datalake-demo_raw_closed_deals" closed_deals
    on (order_items.seller_id = closed_deals.seller_id);
