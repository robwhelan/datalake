SELECT order_reviews.order_id, closed_deals.seller_id, review_score, sdr_id, sr_id
    FROM "toyota-demo-datalake-main-database"."toyota-demo_drop_order_reviews" order_reviews
    join "toyota-demo-datalake-main-database"."toyota-demo_drop_order_items" order_items
    on (order_reviews.order_id = order_items.order_id)
    join "toyota-demo-datalake-main-database"."toyota-demo_drop_closed_deals" closed_deals
    on (order_items.seller_id = closed_deals.seller_id);
