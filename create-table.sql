create table seller_performance(
  lead_behaviour_profile varchar(32),
  review_creation_date varchar(32),
  price double precision,
  product_id varchar(32),
  business_type varchar(32),
  review_answer_timestamp varchar(32),
  review_id varchar(32),
  shipping_limit_date varchar(32),
  _order_id varchar(32),
  business_segment varchar(32),
  freight_value double precision,
  review_comment_title varchar(32),
  sr_id varchar(32),
  order_item_id bigint,
  declared_monthly_revenue double precision,
  review_score bigint,
  sdr_id varchar(32),
  order_id varchar(32),
  review_comment_message varchar(320),
  has_gtin boolean,
  _seller_id varchar(32),
  lead_type varchar(32),
  mql_id varchar(32),
  seller_id varchar(32),
  has_company boolean,
  average_stock varchar(32),
  won_date varchar(32)
)
diststyle even
compound sortkey(seller_id,sr_id);


COPY seller_performance
FROM 's3://datalake-demo-curated-773548596459/seller-performance/'
IAM_ROLE 'arn:aws:iam::773548596459:role/redshiftlabs3'
FORMAT AS PARQUET;

select seller_id, avg(review_score) from public."seller_performance"
group by seller_id
order by avg(review_score) DESC;
