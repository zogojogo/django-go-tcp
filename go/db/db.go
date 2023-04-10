package db

import (
	"entry_task/config"
	"fmt"
	"log"
	"os"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var (
	db *gorm.DB
)

func getLogger() logger.Interface {
	return logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags),
		logger.Config{
			LogLevel: logger.Info,
		},
	)
}

func Connect() (err error) {
	c := config.NewConfig().DBConfig
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&parseTime=True&loc=Local",
		c.User,
		c.Password,
		c.Host,
		c.Port,
		c.DBName,
	)
	db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{
		// Logger: getLogger(),
	})
	if err != nil {
		return
	}
	// set max idle connection
	sqlDB, err := db.DB()
	if err != nil {
		return
	}
	sqlDB.SetMaxIdleConns(10)
	return
}

func Get() *gorm.DB {
	return db
}
