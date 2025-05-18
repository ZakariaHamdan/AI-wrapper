using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class Currency : MainEntity
{
    [MaxLength(255)]
    public string? NameAr { get; set; }
    
    [Required] [MaxLength(255)]
    public string NameEn { get; set; }
    [MaxLength(50)] 
    public string? Code { get; set; } 
    
    public string? Symbol { get; set; }
    
    public decimal? ExchangeRate { get; set; }

}
