-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 29, 2025 at 12:41 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hitman_edge_dev`
--

-- --------------------------------------------------------

--
-- Table structure for table `he_actionsmaster`
--

CREATE TABLE `he_actionsmaster` (
  `action_id` int(11) NOT NULL,
  `action_name` varchar(50) NOT NULL,
  `action_description` varchar(255) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_analystmaster`
--

CREATE TABLE `he_analystmaster` (
  `analyst_id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `expertise_area` varchar(255) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_company`
--

CREATE TABLE `he_company` (
  `company_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `sector` varchar(100) NOT NULL,
  `industry_id` int(11) NOT NULL,
  `country` varchar(50) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `founded_year` int(11) DEFAULT NULL,
  `market_cap` decimal(18,2) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_competitormaster`
--

CREATE TABLE `he_competitormaster` (
  `competitor_master_id` int(11) NOT NULL,
  `main_ticker_id` int(11) NOT NULL,
  `competitor_ticker_1` int(11) DEFAULT NULL,
  `competitor_ticker_2` int(11) DEFAULT NULL,
  `competitor_ticker_3` int(11) DEFAULT NULL,
  `competitor_ticker_4` int(11) DEFAULT NULL,
  `competitor_ticker_5` int(11) DEFAULT NULL,
  `competitor_ticker_6` int(11) DEFAULT NULL,
  `competitor_ticker_7` int(11) DEFAULT NULL,
  `competitor_ticker_8` int(11) DEFAULT NULL,
  `competitor_ticker_9` int(11) DEFAULT NULL,
  `competitor_ticker_10` int(11) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_currencymaster`
--

CREATE TABLE `he_currencymaster` (
  `currency_code` varchar(10) NOT NULL,
  `currency_name` varchar(50) NOT NULL,
  `symbol` varchar(10) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_error_logs`
--

CREATE TABLE `he_error_logs` (
  `id` int(11) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `error_description` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `created_by` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_file`
--

CREATE TABLE `he_file` (
  `id` int(11) NOT NULL,
  `job_name` varchar(100) DEFAULT NULL,
  `file_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `he_file`
--

INSERT INTO `he_file` (`id`, `job_name`, `file_name`) VALUES
(1, 'HE_Average_Cost_Scenarios', 'HE_average_cost_scenarios.py'),
(2, 'HE_Greeks', 'HE_greeks.py'),
(3, 'HE_News', 'HE_news.py'),
(4, 'HE_NewsApi_Org', 'HE_newsapi_org.py'),
(5, 'HE_Options_Trading_Pull_Metrics', 'HE_options_trading_pull_metrics.py'),
(6, 'HE_Portfilio', 'HE_portfilio.py'),
(7, 'HE_Portfilio_Master_Table', 'HE_portfilio_master_table.py'),
(8, 'HE_Scheduler', 'HE_scheduler.py'),
(9, 'HE_Seekingalpha', 'HE_seekingalpha.py'),
(10, 'HE_Straddle_Strategy', 'HE_straddle_strategy.py'),
(11, 'HE_Summarize_Earning_Report', 'HE_summarize_earning_report.py'),
(12, 'HE_Summary', 'HE_summary.py'),
(13, 'HE_Support_Resistance', 'HE_support_resistance.py'),
(14, 'HE_Symbol_Close_Price', 'HE_symbol_close_price.py'),
(15, 'HE_Upcoming_Earning_Report', 'HE_upcoming_earning_report.py'),
(16, 'HE_US_Multiple_Stock_Buy_Sell', 'HE_US\r\n _multiple_stock_buy_sell.py'),
(17, 'HE_Yahoo_Finance', 'HE_yahoo_finance.py'),
(18, 'HE_Yahoo_Finance_1', 'HE_yahoo_finance_1.py'),
(19, 'HE_Yahoo_Finance_News', 'HE_yahoo_finance_news.py'),
(20, 'HE_mail', 'HE_mail.py'),
(21, 'HE_test', 'HE_test.py'),
(22, 'HE_support', 'HE_support.py');

-- --------------------------------------------------------

--
-- Table structure for table `he_index_data`
--

CREATE TABLE `he_index_data` (
  `symbol` varchar(10) NOT NULL,
  `index_name` varchar(50) DEFAULT NULL,
  `close_price` decimal(10,2) DEFAULT NULL,
  `percent_change` decimal(6,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_industry`
--

CREATE TABLE `he_industry` (
  `industry_id` int(11) NOT NULL,
  `sector` varchar(100) NOT NULL,
  `industry` varchar(100) NOT NULL,
  `sub_industry` varchar(100) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_investmentlimitmaster`
--

CREATE TABLE `he_investmentlimitmaster` (
  `limit_id` int(11) NOT NULL,
  `overall_limit_per_stock` decimal(18,2) NOT NULL,
  `position_size_limit` decimal(18,2) NOT NULL,
  `per_transaction_limit` decimal(18,2) NOT NULL,
  `options_trading_limit` decimal(18,2) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_job_execution`
--

CREATE TABLE `he_job_execution` (
  `id` int(11) NOT NULL,
  `job_number` int(11) NOT NULL,
  `job_run_number` int(11) NOT NULL,
  `execution_status` varchar(50) DEFAULT NULL,
  `start_datetime` datetime DEFAULT NULL,
  `end_datetime` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_job_logs`
--

CREATE TABLE `he_job_logs` (
  `job_log_number` int(11) NOT NULL,
  `job_number` int(11) NOT NULL,
  `job_run_number` int(11) NOT NULL,
  `job_log_description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_job_master`
--

CREATE TABLE `he_job_master` (
  `job_number` int(11) NOT NULL,
  `job_name` varchar(255) NOT NULL,
  `schedule_frequency` enum('Daily','Weekly','Monthly') NOT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `schedule_type` varchar(100) DEFAULT NULL,
  `event_condition` varchar(255) DEFAULT NULL,
  `dependent_job_number` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_jonah_compare`
--

CREATE TABLE `he_jonah_compare` (
  `id` int(11) NOT NULL,
  `jonah_ticker` varchar(20) DEFAULT NULL,
  `jonah_category` varchar(50) DEFAULT NULL,
  `jonah_position` decimal(18,4) DEFAULT NULL,
  `he_ticker` varchar(20) DEFAULT NULL,
  `he_category` varchar(50) DEFAULT NULL,
  `position_difference` decimal(18,4) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_lookup`
--

CREATE TABLE `he_lookup` (
  `id` int(11) NOT NULL,
  `code` varchar(100) DEFAULT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `sort_order` int(11) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_news`
--

CREATE TABLE `he_news` (
  `news_id` int(11) NOT NULL,
  `ticker_id` int(11) NOT NULL,
  `headline` varchar(500) NOT NULL,
  `summary` text DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  `published_at` datetime NOT NULL,
  `lang` varchar(10) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `sentiment_label` enum('positive','neutral','negative') DEFAULT 'neutral',
  `sentiment_score` decimal(4,3) DEFAULT NULL,
  `impact_score` decimal(5,2) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_optionscontract`
--

CREATE TABLE `he_optionscontract` (
  `option_id` int(11) NOT NULL,
  `ticker_id` int(11) NOT NULL,
  `symbol` varchar(50) NOT NULL,
  `contract_type` enum('call','put') NOT NULL,
  `expiration_date` date NOT NULL,
  `strike_price` decimal(10,2) NOT NULL,
  `last_price` decimal(10,2) DEFAULT NULL,
  `bid` decimal(10,2) DEFAULT NULL,
  `ask` decimal(10,2) DEFAULT NULL,
  `volume` int(11) DEFAULT 0,
  `open_interest` int(11) DEFAULT 0,
  `implied_volatility` decimal(6,4) DEFAULT NULL,
  `delta` decimal(6,4) DEFAULT NULL,
  `gamma` decimal(6,4) DEFAULT NULL,
  `theta` decimal(6,4) DEFAULT NULL,
  `vega` decimal(6,4) DEFAULT NULL,
  `rho` decimal(6,4) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_optionsmaster`
--

CREATE TABLE `he_optionsmaster` (
  `option_type_id` int(11) NOT NULL,
  `option_type_name` varchar(100) NOT NULL,
  `option_type_description` text DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_options_ibkr`
--

CREATE TABLE `he_options_ibkr` (
  `id` int(11) NOT NULL,
  `Options_Available` int(11) DEFAULT NULL,
  `Premium_Call` decimal(10,2) DEFAULT NULL,
  `Premium_Put` decimal(10,2) DEFAULT NULL,
  `Sell_Call` decimal(10,2) DEFAULT NULL,
  `Buy_Put` decimal(10,2) DEFAULT NULL,
  `Sell_Put` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_option_greeks`
--

CREATE TABLE `he_option_greeks` (
  `id` int(11) NOT NULL,
  `symbol` varchar(10) DEFAULT NULL,
  `option_type` varchar(10) DEFAULT NULL,
  `stock_price` float DEFAULT NULL,
  `strike_price` float DEFAULT NULL,
  `implied_volatility` float DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `today_date` date DEFAULT NULL,
  `time_to_expiry` float DEFAULT NULL,
  `delta` float DEFAULT NULL,
  `gamma` float DEFAULT NULL,
  `theta` float DEFAULT NULL,
  `vega` float DEFAULT NULL,
  `rho` float DEFAULT NULL,
  `risk_free_rate` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_otp_data`
--

CREATE TABLE `he_otp_data` (
  `id` int(11) NOT NULL,
  `email` text NOT NULL,
  `otp` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_portfolio_master`
--

CREATE TABLE `he_portfolio_master` (
  `id` int(11) NOT NULL,
  `ticker` varchar(20) NOT NULL,
  `Category` varchar(50) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `avg_cost` decimal(10,2) DEFAULT NULL,
  `position_size` decimal(10,2) DEFAULT NULL,
  `total_cost` decimal(10,2) DEFAULT NULL,
  `current_price` decimal(10,2) DEFAULT NULL,
  `unrealized_gain_loss` decimal(10,2) DEFAULT NULL,
  `realized_gain_loss` decimal(10,2) DEFAULT NULL,
  `first_buy_age` varchar(100) DEFAULT NULL,
  `avg_age_days` int(11) DEFAULT NULL,
  `platform` varchar(50) DEFAULT NULL,
  `industry_pe` decimal(10,2) DEFAULT NULL,
  `current_pe` decimal(10,2) DEFAULT NULL,
  `price_sales_ratio` decimal(10,2) DEFAULT NULL,
  `price_book_ratio` decimal(10,2) DEFAULT NULL,
  `50_day_ema` decimal(10,2) DEFAULT NULL,
  `100_day_ema` decimal(10,2) DEFAULT NULL,
  `200_day_ema` decimal(10,2) DEFAULT NULL,
  `sp_500_ya` decimal(10,2) DEFAULT NULL,
  `russell_1000_ya` decimal(10,2) DEFAULT NULL,
  `pe_ratio` decimal(10,2) DEFAULT NULL,
  `peg_ratio` decimal(10,2) DEFAULT NULL,
  `roe` decimal(10,2) DEFAULT NULL,
  `net_profit_margin` decimal(10,2) DEFAULT NULL,
  `current_ratio` decimal(10,2) DEFAULT NULL,
  `debt_equity` decimal(10,2) DEFAULT NULL,
  `fcf_yield` decimal(10,2) DEFAULT NULL,
  `revenue_growth` decimal(10,2) DEFAULT NULL,
  `earnings_accuracy` decimal(10,2) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `nasdaq_ya` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_research`
--

CREATE TABLE `he_research` (
  `research_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `report_date` date NOT NULL,
  `fiscal_year` int(11) NOT NULL,
  `fiscal_quarter` enum('Q1','Q2','Q3','Q4') NOT NULL,
  `data_source` varchar(100) DEFAULT NULL,
  `provider_report_id` varchar(100) DEFAULT NULL,
  `pe_ratio` decimal(8,2) DEFAULT NULL,
  `peg_ratio` decimal(8,2) DEFAULT NULL,
  `price_to_book` decimal(8,2) DEFAULT NULL,
  `price_to_sales` decimal(8,2) DEFAULT NULL,
  `enterprise_value` decimal(18,2) DEFAULT NULL,
  `ev_to_ebitda` decimal(8,2) DEFAULT NULL,
  `net_margin` decimal(6,2) DEFAULT NULL,
  `gross_margin` decimal(6,2) DEFAULT NULL,
  `return_on_equity` decimal(6,2) DEFAULT NULL,
  `return_on_assets` decimal(6,2) DEFAULT NULL,
  `debt_to_equity` decimal(6,2) DEFAULT NULL,
  `current_ratio` decimal(6,2) DEFAULT NULL,
  `quick_ratio` decimal(6,2) DEFAULT NULL,
  `interest_coverage` decimal(6,2) DEFAULT NULL,
  `revenue_growth_yoy` decimal(6,2) DEFAULT NULL,
  `earnings_growth_yoy` decimal(6,2) DEFAULT NULL,
  `free_cash_flow` decimal(18,2) DEFAULT NULL,
  `dividend_yield` decimal(6,2) DEFAULT NULL,
  `market_cap` decimal(18,2) DEFAULT NULL,
  `shares_outstanding` bigint(20) DEFAULT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_stockmaster`
--

CREATE TABLE `he_stockmaster` (
  `stock_id` int(11) NOT NULL,
  `ticker` varchar(20) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `industry` varchar(100) DEFAULT NULL,
  `sub_industry` varchar(100) DEFAULT NULL,
  `size` enum('Small Cap','Mid Cap','Large Cap','Very Large Cap') DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_stocks_ibkr`
--

CREATE TABLE `he_stocks_ibkr` (
  `id` int(11) NOT NULL,
  `ticker` varchar(100) NOT NULL,
  `order_id` varchar(100) NOT NULL,
  `quantity` int(11) NOT NULL,
  `avg_cost` decimal(10,2) NOT NULL,
  `Stock_Price` decimal(10,2) NOT NULL,
  `Buy_Qty` int(11) NOT NULL,
  `Sell_Qty` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_stock_transaction`
--

CREATE TABLE `he_stock_transaction` (
  `id` int(1) NOT NULL,
  `ticker` varchar(20) DEFAULT NULL,
  `date` date NOT NULL,
  `trade_type` varchar(10) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `platform` varchar(50) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_technicalindicators`
--

CREATE TABLE `he_technicalindicators` (
  `indicator_id` int(11) NOT NULL,
  `ticker_id` int(11) NOT NULL,
  `option_id` int(11) DEFAULT NULL,
  `timeframe` varchar(10) NOT NULL,
  `timestamp` datetime NOT NULL,
  `macd` decimal(10,5) DEFAULT NULL,
  `macd_signal` decimal(10,5) DEFAULT NULL,
  `macd_hist` decimal(10,5) DEFAULT NULL,
  `rsi` decimal(5,2) DEFAULT NULL,
  `bollinger_upper` decimal(10,2) DEFAULT NULL,
  `bollinger_lower` decimal(10,2) DEFAULT NULL,
  `bollinger_mid` decimal(10,2) DEFAULT NULL,
  `ichimoku_tenkan_sen` decimal(10,2) DEFAULT NULL,
  `ichimoku_kijun_sen` decimal(10,2) DEFAULT NULL,
  `ichimoku_senkou_span_a` decimal(10,2) DEFAULT NULL,
  `ichimoku_senkou_span_b` decimal(10,2) DEFAULT NULL,
  `ichimoku_chikou_span` decimal(10,2) DEFAULT NULL,
  `sma_20` decimal(10,2) DEFAULT NULL,
  `ema_50` decimal(10,2) DEFAULT NULL,
  `data_source` varchar(100) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_ticker`
--

CREATE TABLE `he_ticker` (
  `ticker_id` int(11) NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `company_id` int(11) NOT NULL,
  `exchange` varchar(50) NOT NULL,
  `instrument_type` varchar(20) NOT NULL,
  `currency` varchar(10) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `listed_at` date NOT NULL,
  `delisted_at` date DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_upcoming_earning_report`
--

CREATE TABLE `he_upcoming_earning_report` (
  `id` int(11) NOT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `ticker_symbol` varchar(50) DEFAULT NULL,
  `earnings_date` date DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `eps_estimate` float DEFAULT NULL,
  `actual_eps` float DEFAULT NULL,
  `market_cap` varchar(100) NOT NULL,
  `current_price` varchar(100) NOT NULL,
  `volatility` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `he_usermaster`
--

CREATE TABLE `he_usermaster` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `user_login_id` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `he_actionsmaster`
--
ALTER TABLE `he_actionsmaster`
  ADD PRIMARY KEY (`action_id`),
  ADD UNIQUE KEY `action_name` (`action_name`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_analystmaster`
--
ALTER TABLE `he_analystmaster`
  ADD PRIMARY KEY (`analyst_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_company`
--
ALTER TABLE `he_company`
  ADD PRIMARY KEY (`company_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_industry_id` (`industry_id`),
  ADD KEY `idx_sector` (`sector`);

--
-- Indexes for table `he_competitormaster`
--
ALTER TABLE `he_competitormaster`
  ADD PRIMARY KEY (`competitor_master_id`),
  ADD KEY `main_ticker_id` (`main_ticker_id`),
  ADD KEY `competitor_ticker_1` (`competitor_ticker_1`),
  ADD KEY `competitor_ticker_2` (`competitor_ticker_2`),
  ADD KEY `competitor_ticker_3` (`competitor_ticker_3`),
  ADD KEY `competitor_ticker_4` (`competitor_ticker_4`),
  ADD KEY `competitor_ticker_5` (`competitor_ticker_5`),
  ADD KEY `competitor_ticker_6` (`competitor_ticker_6`),
  ADD KEY `competitor_ticker_7` (`competitor_ticker_7`),
  ADD KEY `competitor_ticker_8` (`competitor_ticker_8`),
  ADD KEY `competitor_ticker_9` (`competitor_ticker_9`),
  ADD KEY `competitor_ticker_10` (`competitor_ticker_10`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_currencymaster`
--
ALTER TABLE `he_currencymaster`
  ADD PRIMARY KEY (`currency_code`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_error_logs`
--
ALTER TABLE `he_error_logs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `he_file`
--
ALTER TABLE `he_file`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `he_index_data`
--
ALTER TABLE `he_index_data`
  ADD PRIMARY KEY (`symbol`);

--
-- Indexes for table `he_industry`
--
ALTER TABLE `he_industry`
  ADD PRIMARY KEY (`industry_id`),
  ADD UNIQUE KEY `uniq_sector_industry_subindustry` (`sector`,`industry`,`sub_industry`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_investmentlimitmaster`
--
ALTER TABLE `he_investmentlimitmaster`
  ADD PRIMARY KEY (`limit_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_job_execution`
--
ALTER TABLE `he_job_execution`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_exec_job` (`job_number`),
  ADD KEY `fk_exec_created_by` (`created_by`),
  ADD KEY `fk_exec_updated_by` (`updated_by`);

--
-- Indexes for table `he_job_logs`
--
ALTER TABLE `he_job_logs`
  ADD PRIMARY KEY (`job_log_number`),
  ADD KEY `fk_logs_job` (`job_number`),
  ADD KEY `fk_logs_created_by` (`created_by`),
  ADD KEY `fk_logs_updated_by` (`updated_by`);

--
-- Indexes for table `he_job_master`
--
ALTER TABLE `he_job_master`
  ADD PRIMARY KEY (`job_number`),
  ADD KEY `fk_dep_job` (`dependent_job_number`),
  ADD KEY `fk_job_created_by` (`created_by`),
  ADD KEY `fk_job_updated_by` (`updated_by`);

--
-- Indexes for table `he_jonah_compare`
--
ALTER TABLE `he_jonah_compare`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_jonahcompare_created_by` (`created_by`),
  ADD KEY `fk_jonahcompare_updated_by` (`updated_by`);

--
-- Indexes for table `he_lookup`
--
ALTER TABLE `he_lookup`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `he_news`
--
ALTER TABLE `he_news`
  ADD PRIMARY KEY (`news_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_ticker_id` (`ticker_id`),
  ADD KEY `idx_published_at` (`published_at`);

--
-- Indexes for table `he_optionscontract`
--
ALTER TABLE `he_optionscontract`
  ADD PRIMARY KEY (`option_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_ticker_id` (`ticker_id`),
  ADD KEY `idx_expiration_date` (`expiration_date`);

--
-- Indexes for table `he_optionsmaster`
--
ALTER TABLE `he_optionsmaster`
  ADD PRIMARY KEY (`option_type_id`),
  ADD UNIQUE KEY `option_type_name` (`option_type_name`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_options_ibkr`
--
ALTER TABLE `he_options_ibkr`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_he_options_ibkr_created_by` (`created_by`),
  ADD KEY `fk_he_options_ibkr_updated_by` (`updated_by`);

--
-- Indexes for table `he_option_greeks`
--
ALTER TABLE `he_option_greeks`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `he_otp_data`
--
ALTER TABLE `he_otp_data`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`) USING HASH;

--
-- Indexes for table `he_portfolio_master`
--
ALTER TABLE `he_portfolio_master`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_ticker_user` (`ticker`,`created_by`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_research`
--
ALTER TABLE `he_research`
  ADD PRIMARY KEY (`research_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_company_id` (`company_id`),
  ADD KEY `idx_report_date` (`report_date`);

--
-- Indexes for table `he_stockmaster`
--
ALTER TABLE `he_stockmaster`
  ADD PRIMARY KEY (`stock_id`),
  ADD UNIQUE KEY `uniq_ticker` (`ticker`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `he_stocks_ibkr`
--
ALTER TABLE `he_stocks_ibkr`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_he_stocks_ibkr_created_by` (`created_by`),
  ADD KEY `fk_he_stocks_ibkr_updated_by` (`updated_by`);

--
-- Indexes for table `he_stock_transaction`
--
ALTER TABLE `he_stock_transaction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_created_by` (`created_by`),
  ADD KEY `fk_updated_by` (`updated_by`);

--
-- Indexes for table `he_technicalindicators`
--
ALTER TABLE `he_technicalindicators`
  ADD PRIMARY KEY (`indicator_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_ticker_id` (`ticker_id`),
  ADD KEY `idx_option_id` (`option_id`),
  ADD KEY `idx_timestamp` (`timestamp`);

--
-- Indexes for table `he_ticker`
--
ALTER TABLE `he_ticker`
  ADD PRIMARY KEY (`ticker_id`),
  ADD UNIQUE KEY `uniq_symbol_exchange` (`symbol`,`exchange`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `idx_company_id` (`company_id`);

--
-- Indexes for table `he_usermaster`
--
ALTER TABLE `he_usermaster`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_name` (`user_name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `he_actionsmaster`
--
ALTER TABLE `he_actionsmaster`
  MODIFY `action_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `he_analystmaster`
--
ALTER TABLE `he_analystmaster`
  MODIFY `analyst_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_company`
--
ALTER TABLE `he_company`
  MODIFY `company_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `he_competitormaster`
--
ALTER TABLE `he_competitormaster`
  MODIFY `competitor_master_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `he_error_logs`
--
ALTER TABLE `he_error_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_file`
--
ALTER TABLE `he_file`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `he_industry`
--
ALTER TABLE `he_industry`
  MODIFY `industry_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_investmentlimitmaster`
--
ALTER TABLE `he_investmentlimitmaster`
  MODIFY `limit_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_job_execution`
--
ALTER TABLE `he_job_execution`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_job_logs`
--
ALTER TABLE `he_job_logs`
  MODIFY `job_log_number` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_job_master`
--
ALTER TABLE `he_job_master`
  MODIFY `job_number` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_jonah_compare`
--
ALTER TABLE `he_jonah_compare`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_lookup`
--
ALTER TABLE `he_lookup`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_news`
--
ALTER TABLE `he_news`
  MODIFY `news_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_optionscontract`
--
ALTER TABLE `he_optionscontract`
  MODIFY `option_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_optionsmaster`
--
ALTER TABLE `he_optionsmaster`
  MODIFY `option_type_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_options_ibkr`
--
ALTER TABLE `he_options_ibkr`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_otp_data`
--
ALTER TABLE `he_otp_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_portfolio_master`
--
ALTER TABLE `he_portfolio_master`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_research`
--
ALTER TABLE `he_research`
  MODIFY `research_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_stockmaster`
--
ALTER TABLE `he_stockmaster`
  MODIFY `stock_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `he_stocks_ibkr`
--
ALTER TABLE `he_stocks_ibkr`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_stock_transaction`
--
ALTER TABLE `he_stock_transaction`
  MODIFY `id` int(1) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_technicalindicators`
--
ALTER TABLE `he_technicalindicators`
  MODIFY `indicator_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_ticker`
--
ALTER TABLE `he_ticker`
  MODIFY `ticker_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `he_usermaster`
--
ALTER TABLE `he_usermaster`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `he_actionsmaster`
--
ALTER TABLE `he_actionsmaster`
  ADD CONSTRAINT `he_actionsmaster_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_actionsmaster_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `he_company`
--
ALTER TABLE `he_company`
  ADD CONSTRAINT `he_company_ibfk_1` FOREIGN KEY (`industry_id`) REFERENCES `he_industry` (`industry_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_company_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `he_usermaster` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `he_company_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `he_usermaster` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
