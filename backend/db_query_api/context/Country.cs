using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class Country : MainEntity
{
    [MaxLength(255)]
    public string? NameAr { get; set; }
    
    [Required] [MaxLength(255)]
    public string NameEn { get; set; }
    [MaxLength(50)] 
    public string? Code { get; set; } 
    
    public string? PhoneCode { get; set; }
    
    public Guid? CurrencyId { get; set; }

    
    
    public Currency? Currency { get; set; }
    public List<City>? Cities { get; set; } = new List<City>(); 
    public List<Region>? Regions { get; set; } = new List<Region>(); 
}