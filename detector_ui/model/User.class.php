<?php
	class User { 
		private $uuid='';
		private $shop='';
		private $password='';
		private $token='';
		private $timestamp='';
		private $id='';

		/**
		 * @return string
		 */
		public function getUuid()
		{
			return $this->uuid;
		}

		/**
		 * @param string $uuid
		 */
		public function setUuid($uuid)
		{
			$this->uuid = $uuid;
		}

		/**
		 * @return string
		 */
		public function getShop()
		{
			return $this->shop;
		}

		/**
		 * @param string $shop
		 */
		public function setShop($shop)
		{
			$this->shop = $shop;
		}

		/**
		 * @return string
		 */
		public function getPassword()
		{
			return $this->password;
		}

		/**
		 * @param string $password
		 */
		public function setPassword($password)
		{
			$this->password = $password;
		}

		/**
		 * @return string
		 */
		public function getToken()
		{
			return $this->token;
		}

		/**
		 * @param string $token
		 */
		public function setToken($token)
		{
			$this->token = $token;
		}

		/**
		 * @return string
		 */
		public function getTimestamp()
		{
			return $this->timestamp;
		}

		/**
		 * @param string $timestamp
		 */
		public function setTimestamp($timestamp)
		{
			$this->timestamp = $timestamp;
		}

		/**
		 * @return string
		 */
		public function getId()
		{
			return $this->id;
		}

		/**
		 * @param string $id
		 */
		public function setId($id)
		{
			$this->id = $id;
		}

	} 

?>

